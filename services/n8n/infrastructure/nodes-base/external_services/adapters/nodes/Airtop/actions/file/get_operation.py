"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/file/get.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../constants、../../transport、../transport/types。导出:description。关键函数/方法:execute、response、buffer。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/file/get.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/file/get_operation.py

import { NodeOperationError } from 'n8n-workflow';
import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';

import { ERROR_MESSAGES } from '../../constants';
import { apiRequest } from '../../transport';
import type { IAirtopResponseWithFiles } from '../../transport/types';

const displayOptions = {
	show: {
		resource: ['file'],
		operation: ['get'],
	},
};

export const description: INodeProperties[] = [
	{
		displayName: 'File ID',
		name: 'fileId',
		type: 'string',
		default: '',
		required: true,
		description: 'ID of the file to retrieve',
		displayOptions,
	},
	{
		displayName: 'Output Binary File',
		name: 'outputBinaryFile',
		type: 'boolean',
		default: false,
		description: 'Whether to output the file in binary format if the file is ready for download',
		displayOptions,
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const fileId = this.getNodeParameter('fileId', index, '') as string;
	const outputBinaryFile = this.getNodeParameter('outputBinaryFile', index, false);

	if (!fileId) {
		throw new NodeOperationError(
			this.getNode(),
			ERROR_MESSAGES.REQUIRED_PARAMETER.replace('{{field}}', 'File ID'),
		);
	}

	const response = (await apiRequest.call(
		this,
		'GET',
		`/files/${fileId}`,
	)) as IAirtopResponseWithFiles;

	const { fileName = '', downloadUrl = '', status = '' } = response?.data ?? {};

	// Handle binary file output
	if (outputBinaryFile && downloadUrl && status === 'available') {
		const buffer = (await this.helpers.httpRequest({
			url: downloadUrl,
			json: false,
			encoding: 'arraybuffer',
		})) as Buffer;
		const file = await this.helpers.prepareBinaryData(buffer, fileName);
		return [
			{
				json: {
					...response,
				},
				binary: { data: file },
			},
		];
	}

	return this.helpers.returnJsonArray({ ...response });
}
