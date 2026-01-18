"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/actions/file/get.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Anthropic 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/interfaces、../helpers/utils、../../transport。导出:properties、description。关键函数/方法:execute、response。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/actions/file/get.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Anthropic/actions/file/get_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import type { File } from '../../helpers/interfaces';
import { getBaseUrl } from '../../helpers/utils';
import { apiRequest } from '../../transport';

export const properties: INodeProperties[] = [
	{
		displayName: 'File ID',
		name: 'fileId',
		type: 'string',
		placeholder: 'e.g. file_123',
		description: 'ID of the file to get metadata for',
		default: '',
	},
];

const displayOptions = {
	show: {
		operation: ['get'],
		resource: ['file'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const fileId = this.getNodeParameter('fileId', i, '') as string;
	const baseUrl = await getBaseUrl.call(this);
	const response = (await apiRequest.call(this, 'GET', `/v1/files/${fileId}`)) as File;
	return [
		{
			json: { ...response, url: `${baseUrl}/v1/files/${response.id}` },
			pairedItem: { item: i },
		},
	];
}
