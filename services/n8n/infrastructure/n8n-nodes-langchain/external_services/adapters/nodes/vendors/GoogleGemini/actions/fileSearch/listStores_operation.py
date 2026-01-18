"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/fileSearch/listStores.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils。导出:properties、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/fileSearch/listStores.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/GoogleGemini/actions/fileSearch/listStores_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { listFileSearchStores } from '../../helpers/utils';

export const properties: INodeProperties[] = [
	{
		displayName: 'Page Size',
		name: 'pageSize',
		type: 'number',
		description: 'Maximum number of File Search stores to return per page (max 20)',
		default: 10,
		typeOptions: {
			minValue: 1,
			maxValue: 20,
		},
	},
	{
		displayName: 'Page Token',
		name: 'pageToken',
		// eslint-disable-next-line -- pageToken is a pagination token, not a password
		type: 'string',
		description: 'Token from a previous page to retrieve the next page of results',
		default: '',
	},
];

const displayOptions = {
	show: {
		operation: ['listStores'],
		resource: ['fileSearch'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const pageSize = this.getNodeParameter('pageSize', i) as number | undefined;
	const pageToken = this.getNodeParameter('pageToken', i, '') as string | undefined;

	const response = await listFileSearchStores.call(this, pageSize, pageToken);
	return [
		{
			json: response,
			pairedItem: {
				item: i,
			},
		},
	];
}
