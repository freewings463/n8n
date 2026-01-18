"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/fileSearch/deleteStore.operation.ts
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
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/fileSearch/deleteStore.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/GoogleGemini/actions/fileSearch/deleteStore_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { deleteFileSearchStore } from '../../helpers/utils';

export const properties: INodeProperties[] = [
	{
		displayName: 'File Search Store Name',
		name: 'fileSearchStoreName',
		type: 'string',
		placeholder: 'e.g. fileSearchStores/abc123',
		description: 'The full name of the File Search store to delete (format: fileSearchStores/...)',
		default: '',
		required: true,
	},
	{
		displayName: 'Force Delete',
		name: 'force',
		type: 'boolean',
		description:
			'Whether to delete related Documents and objects. If false, deletion will fail if the store contains any Documents.',
		default: false,
	},
];

const displayOptions = {
	show: {
		operation: ['deleteStore'],
		resource: ['fileSearch'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const fileSearchStoreName = this.getNodeParameter('fileSearchStoreName', i, '') as string;
	const force = this.getNodeParameter('force', i, false) as boolean | undefined;

	const response = await deleteFileSearchStore.call(this, fileSearchStoreName, force);
	return [
		{
			json: response,
			pairedItem: {
				item: i,
			},
		},
	];
}
