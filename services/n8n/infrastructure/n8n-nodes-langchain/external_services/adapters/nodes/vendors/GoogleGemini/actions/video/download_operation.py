"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/video/download.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/video/download.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/GoogleGemini/actions/video/download_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { downloadFile } from '../../helpers/utils';

const properties: INodeProperties[] = [
	{
		displayName: 'URL',
		name: 'url',
		type: 'string',
		placeholder: 'e.g. https://generativelanguage.googleapis.com/v1beta/files/abcdefg:download',
		description: 'The URL from Google Gemini API to download the video from',
		default: '',
	},
	{
		displayName: 'Options',
		name: 'options',
		placeholder: 'Add Option',
		type: 'collection',
		default: {},
		options: [
			{
				displayName: 'Put Output in Field',
				name: 'binaryPropertyOutput',
				type: 'string',
				default: 'data',
				hint: 'The name of the output field to put the binary file data in',
			},
		],
	},
];

const displayOptions = {
	show: {
		operation: ['download'],
		resource: ['video'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const url = this.getNodeParameter('url', i, '') as string;
	const binaryPropertyOutput = this.getNodeParameter(
		'options.binaryPropertyOutput',
		i,
		'data',
	) as string;
	const credentials = await this.getCredentials('googlePalmApi');
	const { fileContent, mimeType } = await downloadFile.call(this, url, 'video/mp4', {
		key: credentials.apiKey as string,
	});
	const binaryData = await this.helpers.prepareBinaryData(fileContent, 'video.mp4', mimeType);
	return [
		{
			binary: { [binaryPropertyOutput]: binaryData },
			json: {
				...binaryData,
				data: undefined,
			},
			pairedItem: { item: i },
		},
	];
}
