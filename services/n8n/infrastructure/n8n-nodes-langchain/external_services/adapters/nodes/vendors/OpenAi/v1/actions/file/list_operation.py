"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/file/list.operation.ts
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
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/file/list.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v1/actions/file/list_operation.py

import type {
	IDataObject,
	INodeProperties,
	IExecuteFunctions,
	INodeExecutionData,
} from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { apiRequest } from '../../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Options',
		name: 'options',
		placeholder: 'Add Option',
		type: 'collection',
		default: {},
		options: [
			{
				displayName: 'Purpose',
				name: 'purpose',
				type: 'options',
				default: 'any',
				description: 'Only return files with the given purpose',
				options: [
					{
						name: 'Any [Default]',
						value: 'any',
					},
					{
						name: 'Assistants',
						value: 'assistants',
					},
					{
						name: 'Fine-Tune',
						value: 'fine-tune',
					},
				],
			},
		],
	},
];

const displayOptions = {
	show: {
		operation: ['list'],
		resource: ['file'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const options = this.getNodeParameter('options', i, {});
	const qs: IDataObject = {};

	if (options.purpose && options.purpose !== 'any') {
		qs.purpose = options.purpose as string;
	}

	const { data } = await apiRequest.call(this, 'GET', '/files', { qs });

	return (data || []).map((file: IDataObject) => ({
		json: file,
		pairedItem: { item: i },
	}));
}
