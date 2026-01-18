"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/actions/prompt/generate.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Anthropic 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/interfaces、../../transport。导出:description。关键函数/方法:execute、response。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/actions/prompt/generate.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Anthropic/actions/prompt/generate_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import type { PromptResponse } from '../../helpers/interfaces';
import { apiRequest } from '../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Task',
		name: 'task',
		type: 'string',
		description: "Description of the prompt's purpose",
		placeholder: 'e.g. A chef for a meal prep planning service',
		default: '',
		typeOptions: {
			rows: 2,
		},
	},
	{
		displayName: 'Simplify Output',
		name: 'simplify',
		type: 'boolean',
		default: true,
		description: 'Whether to return a simplified version of the response instead of the raw data',
	},
];

const displayOptions = {
	show: {
		operation: ['generate'],
		resource: ['prompt'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const task = this.getNodeParameter('task', i, '') as string;
	const simplify = this.getNodeParameter('simplify', i, true) as boolean;

	const body = {
		task,
	};
	const response = (await apiRequest.call(this, 'POST', '/v1/experimental/generate_prompt', {
		body,
		enableAnthropicBetas: { promptTools: true },
	})) as PromptResponse;

	if (simplify) {
		return [
			{
				json: {
					messages: response.messages,
					system: response.system,
				},
				pairedItem: { item: i },
			},
		];
	}

	return [
		{
			json: { ...response },
			pairedItem: { item: i },
		},
	];
}
