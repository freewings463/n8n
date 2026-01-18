"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/assistant/list.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/assistant/list.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v1/actions/assistant/list_operation.py

import type { INodeProperties, IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { apiRequest } from '../../../transport';

const properties: INodeProperties[] = [
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
		operation: ['list'],
		resource: ['assistant'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const returnData: INodeExecutionData[] = [];

	let has_more = true;
	let after: string | undefined;

	do {
		const response = await apiRequest.call(this, 'GET', '/assistants', {
			headers: {
				'OpenAI-Beta': 'assistants=v2',
			},
			qs: {
				limit: 100,
				after,
			},
		});

		for (const assistant of response.data || []) {
			try {
				assistant.created_at = new Date(assistant.created_at * 1000).toISOString();
			} catch (error) {}

			returnData.push({ json: assistant, pairedItem: { item: i } });
		}

		has_more = response.has_more;

		if (has_more) {
			after = response.last_id as string;
		} else {
			break;
		}
	} while (has_more);

	const simplify = this.getNodeParameter('simplify', i) as boolean;

	if (simplify) {
		return returnData.map((item) => {
			const { id, name, model } = item.json;
			return {
				json: {
					id,
					name,
					model,
				},
				pairedItem: { item: i },
			};
		});
	}

	return returnData;
}
