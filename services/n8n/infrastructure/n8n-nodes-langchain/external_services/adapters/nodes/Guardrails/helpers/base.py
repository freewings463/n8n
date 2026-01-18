"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/Guardrails/helpers/base.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/Guardrails/helpers 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:wrapInGuardrailError、runStageGuardrails。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/Guardrails/helpers/base.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/Guardrails/helpers/base.py

import {
	type GuardrailResult,
	GuardrailError,
	type GroupedGuardrailResults,
	type StageGuardRails,
} from '../actions/types';

type RunStageGuardrailsOptions = {
	stageGuardrails: StageGuardRails;
	stage: keyof StageGuardRails;
	inputText: string;
	failOnlyOnErrors?: boolean;
};

// eslint-disable-next-line @typescript-eslint/promise-function-async
const wrapInGuardrailError = (guardrailName: string, promise: Promise<GuardrailResult>) => {
	return promise.catch((error) => {
		throw new GuardrailError(
			guardrailName,
			error?.description || error?.message || 'Unknown error',
			error?.description,
		);
	});
};

export async function runStageGuardrails({
	stageGuardrails,
	stage,
	inputText,
	failOnlyOnErrors,
}: RunStageGuardrailsOptions): Promise<GroupedGuardrailResults> {
	const guardrailPromises: Array<Promise<GuardrailResult>> = [];
	for (const guardrail of stageGuardrails[stage]) {
		guardrailPromises.push(
			wrapInGuardrailError(
				guardrail.name,
				// ensure the check is async
				Promise.resolve().then(async () => await guardrail.check(inputText)),
			),
		);
	}
	const results = await Promise.allSettled(guardrailPromises);
	const passed: Array<PromiseFulfilledResult<GuardrailResult>> = [];
	const failed: Array<PromiseRejectedResult | PromiseFulfilledResult<GuardrailResult>> = [];
	for (const result of results) {
		const checkFailed = failOnlyOnErrors
			? result.status === 'rejected' || !!result.value.executionFailed
			: result.status === 'rejected' || !!result.value.tripwireTriggered;
		if (result.status === 'fulfilled' && !checkFailed) {
			passed.push(result);
		} else {
			failed.push(result);
		}
	}
	return { passed, failed };
}
