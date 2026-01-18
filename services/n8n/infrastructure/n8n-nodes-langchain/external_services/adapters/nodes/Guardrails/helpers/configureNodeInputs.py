"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/Guardrails/helpers/configureNodeInputs.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/Guardrails/helpers 的节点。导入/依赖:外部:无；内部:无；本地:../actions/types。导出:hasLLMGuardrails、configureNodeInputsV2、configureNodeInputsV1。关键函数/方法:hasLLMGuardrails、configureNodeInputsV2、configureNodeInputsV1。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/Guardrails/helpers/configureNodeInputs.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/Guardrails/helpers/configureNodeInputs.py

import type { GuardrailsOptions } from '../actions/types';

const LLM_CHECKS = ['nsfw', 'topicalAlignment', 'custom', 'jailbreak'] as const satisfies Array<
	keyof GuardrailsOptions
>;

export const hasLLMGuardrails = (guardrails: GuardrailsOptions) => {
	const checks = Object.keys(guardrails ?? {});
	return checks.some((check) => (LLM_CHECKS as string[]).includes(check));
};

export const configureNodeInputsV2 = (parameters: { guardrails: GuardrailsOptions }) => {
	// typeof LLM_CHECKS guarantees that it's in sync with hasLLMGuardrails
	const CHECKS: typeof LLM_CHECKS = ['nsfw', 'topicalAlignment', 'custom', 'jailbreak'];
	const checks = Object.keys(parameters?.guardrails ?? {});
	const hasLLMChecks = checks.some((check) => (CHECKS as string[]).includes(check));
	if (!hasLLMChecks) {
		return ['main'];
	}

	return [
		'main',
		{
			type: 'ai_languageModel',
			displayName: 'Chat Model',
			maxConnections: 1,
			required: true,
			filter: {
				excludedNodes: [
					'@n8n/n8n-nodes-langchain.lmCohere',
					'@n8n/n8n-nodes-langchain.lmOllama',
					'n8n/n8n-nodes-langchain.lmOpenAi',
					'@n8n/n8n-nodes-langchain.lmOpenHuggingFaceInference',
				],
			},
		},
	];
};

export const configureNodeInputsV1 = (operation: 'classify' | 'sanitize') => {
	if (operation === 'sanitize') {
		// sanitize operations don't use a chat model
		return ['main'];
	}

	return [
		'main',
		{
			type: 'ai_languageModel',
			displayName: 'Chat Model',
			maxConnections: 1,
			required: true,
			filter: {
				excludedNodes: [
					'@n8n/n8n-nodes-langchain.lmCohere',
					'@n8n/n8n-nodes-langchain.lmOllama',
					'n8n/n8n-nodes-langchain.lmOpenAi',
					'@n8n/n8n-nodes-langchain.lmOpenHuggingFaceInference',
				],
			},
		},
	];
};
