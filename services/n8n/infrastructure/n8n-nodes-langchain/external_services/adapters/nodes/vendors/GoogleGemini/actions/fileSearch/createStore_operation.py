"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/fileSearch/createStore.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini 的Store。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils。导出:properties、description。关键函数/方法:execute。用于管理该模块前端状态（state/actions/getters）供UI消费。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/fileSearch/createStore.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/GoogleGemini/actions/fileSearch/createStore_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { createFileSearchStore } from '../../helpers/utils';

export const properties: INodeProperties[] = [
	{
		displayName: 'Display Name',
		name: 'displayName',
		type: 'string',
		placeholder: 'e.g. My File Search Store',
		description: 'A human-readable name for the File Search store',
		default: '',
		required: true,
	},
];

const displayOptions = {
	show: {
		operation: ['createStore'],
		resource: ['fileSearch'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const displayName = this.getNodeParameter('displayName', i, '') as string;

	const response = await createFileSearchStore.call(this, displayName);
	return [
		{
			json: response,
			pairedItem: {
				item: i,
			},
		},
	];
}
