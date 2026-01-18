"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/Guardrails/helpers/mappers.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/Guardrails/helpers 的节点。导入/依赖:外部:lodash/omit；内部:无；本地:../actions/types。导出:mapGuardrailResultToUserResult、mapGuardrailErrorsToMessage、wrapResultsToNodeExecutionData。关键函数/方法:mapGuardrailResultToUserResult、formatInfo、mapGuardrailErrorsToMessage、wrapResultsToNodeExecutionData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/Guardrails/helpers/mappers.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/Guardrails/helpers/mappers.py

import omit from 'lodash/omit';

import { GuardrailError, type GuardrailResult, type GuardrailUserResult } from '../actions/types';

export const mapGuardrailResultToUserResult = (
	result: GuardrailResult | PromiseSettledResult<GuardrailResult>,
): GuardrailUserResult => {
	const formatInfo = (info?: Record<string, unknown>) => {
		return omit(info ?? {}, ['maskEntities']);
	};
	if ('status' in result) {
		if (result.status === 'fulfilled') {
			return {
				name: result.value.guardrailName,
				triggered: result.value.tripwireTriggered,
				confidenceScore: result.value.confidenceScore,
				executionFailed: result.value.executionFailed,
				exception: result.value.originalException
					? {
							name: result.value.originalException.name,
							description: result.value.originalException.message,
						}
					: undefined,
				info: formatInfo(result.value.info),
			};
		} else {
			return {
				name:
					result.reason instanceof GuardrailError
						? result.reason.guardrailName
						: 'Unknown Guardrail',
				triggered: true,
				executionFailed: true,
				exception:
					result.reason instanceof Error
						? { name: result.reason.name, description: result.reason.message }
						: { name: 'Unknown Exception', description: 'Unknown exception occurred' },
			};
		}
	}
	return {
		name: result.guardrailName,
		triggered: result.tripwireTriggered,
		confidenceScore: result.confidenceScore,
		executionFailed: result.executionFailed,
		exception: result.originalException
			? {
					name: result.originalException.name,
					description: result.originalException.message,
				}
			: undefined,
		info: formatInfo(result.info),
	};
};

export const mapGuardrailErrorsToMessage = (
	results: Array<PromiseSettledResult<GuardrailResult>>,
) => {
	const failedChecks = results
		.filter((r) => r.status === 'rejected' || (r.status === 'fulfilled' && r.value.executionFailed))
		.map((result) => {
			const originalException =
				result.status === 'rejected' ? result.reason : result.value.originalException;
			const message = originalException?.message ?? 'Unknown exception occurred';
			const guardrailName =
				result.status === 'rejected'
					? (originalException?.guardrailName ?? 'Unknown Guardrail')
					: result.value.guardrailName;
			return `${guardrailName} - ${message}`;
		})
		.join(',\n');
	return `Failed checks:\n${failedChecks}`;
};

export const wrapResultsToNodeExecutionData = (
	checks: GuardrailUserResult[],
	itemIndex: number,
) => {
	return checks.length > 0
		? [
				{
					json: { checks },
					pairedItem: { item: itemIndex },
				},
			]
		: [];
};
