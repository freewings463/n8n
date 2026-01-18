"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/file/delete.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../constants、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/file/delete.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/file/delete_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import { ERROR_MESSAGES } from '../../constants';
import { apiRequest } from '../../transport';

export const description: INodeProperties[] = [
	{
		displayName: 'File ID',
		name: 'fileId',
		type: 'string',
		default: '',
		required: true,
		description: 'ID of the file to delete',
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['deleteFile'],
			},
		},
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const fileId = this.getNodeParameter('fileId', index, '') as string;

	if (!fileId) {
		throw new NodeOperationError(
			this.getNode(),
			ERROR_MESSAGES.REQUIRED_PARAMETER.replace('{{field}}', 'File ID'),
		);
	}

	await apiRequest.call(this, 'DELETE', `/files/${fileId}`);

	return this.helpers.returnJsonArray({ data: { message: 'File deleted successfully' } });
}
