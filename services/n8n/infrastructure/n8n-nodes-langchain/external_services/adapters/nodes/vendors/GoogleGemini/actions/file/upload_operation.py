"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/file/upload.operation.ts
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
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/file/upload.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/GoogleGemini/actions/file/upload_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { transferFile } from '../../helpers/utils';

export const properties: INodeProperties[] = [
	{
		displayName: 'Input Type',
		name: 'inputType',
		type: 'options',
		default: 'url',
		options: [
			{
				name: 'File URL',
				value: 'url',
			},
			{
				name: 'Binary File',
				value: 'binary',
			},
		],
	},
	{
		displayName: 'URL',
		name: 'fileUrl',
		type: 'string',
		placeholder: 'e.g. https://example.com/file.pdf',
		description: 'URL of the file to upload',
		default: '',
		displayOptions: {
			show: {
				inputType: ['url'],
			},
		},
	},
	{
		displayName: 'Input Data Field Name',
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		placeholder: 'e.g. data',
		hint: 'The name of the input field containing the binary file data to be processed',
		description: 'Name of the binary property which contains the file',
		displayOptions: {
			show: {
				inputType: ['binary'],
			},
		},
	},
];

const displayOptions = {
	show: {
		operation: ['upload'],
		resource: ['file'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const inputType = this.getNodeParameter('inputType', i, 'url') as string;

	let fileUrl: string | undefined;
	if (inputType === 'url') {
		fileUrl = this.getNodeParameter('fileUrl', i, '') as string;
	}

	const response = await transferFile.call(this, i, fileUrl, 'application/octet-stream');
	return [
		{
			json: response,
			pairedItem: {
				item: i,
			},
		},
	];
}
