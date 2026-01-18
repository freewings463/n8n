"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/V2/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:getInputs。关键函数/方法:getInputs、getInputData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:Function used in the inputs expression to figure out which inputs to。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/V2/utils.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/V2/utils.py

// Function used in the inputs expression to figure out which inputs to

import {
	type INodeInputConfiguration,
	type INodeInputFilter,
	type NodeConnectionType,
} from 'n8n-workflow';

// display based on the agent type
export function getInputs(
	hasMainInput?: boolean,
	hasOutputParser?: boolean,
	needsFallback?: boolean,
): Array<NodeConnectionType | INodeInputConfiguration> {
	interface SpecialInput {
		type: NodeConnectionType;
		filter?: INodeInputFilter;
		displayName: string;
		required?: boolean;
	}

	const getInputData = (
		inputs: SpecialInput[],
	): Array<NodeConnectionType | INodeInputConfiguration> => {
		return inputs.map(({ type, filter, displayName, required }) => {
			const input: INodeInputConfiguration = {
				type,
				displayName,
				required,
				maxConnections: ['ai_languageModel', 'ai_memory', 'ai_outputParser'].includes(type)
					? 1
					: undefined,
			};

			if (filter) {
				input.filter = filter;
			}

			return input;
		});
	};

	let specialInputs: SpecialInput[] = [
		{
			type: 'ai_languageModel',
			displayName: 'Chat Model',
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
		{
			type: 'ai_languageModel',
			displayName: 'Fallback Model',
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
		{
			displayName: 'Memory',
			type: 'ai_memory',
		},
		{
			displayName: 'Tool',
			type: 'ai_tool',
		},
		{
			displayName: 'Output Parser',
			type: 'ai_outputParser',
		},
	];

	if (hasOutputParser === false) {
		specialInputs = specialInputs.filter((input) => input.type !== 'ai_outputParser');
	}
	if (needsFallback === false) {
		specialInputs = specialInputs.filter((input) => input.displayName !== 'Fallback Model');
	}

	// Note cannot use NodeConnectionType.Main
	// otherwise expression won't evaluate correctly on the FE
	const mainInputs = hasMainInput ? ['main' as NodeConnectionType] : [];
	return [...mainInputs, ...getInputData(specialInputs)];
}
