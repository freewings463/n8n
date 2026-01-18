"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/video/generate.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:form-data；内部:n8n-workflow；本地:../helpers/binary-data、../helpers/interfaces、../helpers/polling、../../transport 等1项。导出:description。关键函数/方法:execute、modelRLC、waitSeconds、response、async。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/video/generate.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v2/actions/video/generate_operation.py

import FormData from 'form-data';
import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { NodeOperationError, updateDisplayOptions } from 'n8n-workflow';

import { getBinaryDataFile } from '../../../helpers/binary-data';
import type { VideoJob } from '../../../helpers/interfaces';
import { pollUntilAvailable } from '../../../helpers/polling';
import { apiRequest } from '../../../transport';
import { modelRLC } from '../descriptions';

const properties: INodeProperties[] = [
	modelRLC('videoModelSearch'),
	{
		displayName: 'Prompt',
		name: 'prompt',
		type: 'string',
		default: 'A video of a cat playing with a ball',
		description: 'The prompt to generate a video from',
		required: true,
		typeOptions: {
			rows: 2,
		},
	},
	{
		displayName: 'Seconds',
		name: 'seconds',
		type: 'number',
		default: 4,
		description: 'Clip duration in seconds',
		required: true,
	},
	{
		displayName: 'Size',
		name: 'size',
		type: 'options',
		default: '1280x720',
		description:
			'Output resolution formatted as width x height. 1024x1792 and 1792x1024 are only supported by Sora 2 Pro.',
		options: [
			{ name: '720x1280', value: '720x1280' },
			{ name: '1280x720', value: '1280x720' },
			{ name: '1024x1792', value: '1024x1792' },
			{ name: '1792x1024', value: '1792x1024' },
		],
	},
	{
		displayName: 'Options',
		name: 'options',
		placeholder: 'Add Option',
		type: 'collection',
		default: {},
		options: [
			{
				displayName: 'Reference',
				description: 'Optional image reference that guides generation',
				name: 'binaryPropertyNameReference',
				type: 'string',
				default: 'data',
				placeholder: 'e.g. data',
			},
			{
				displayName: 'Wait Timeout',
				name: 'waitTime',
				type: 'number',
				default: 300,
				description: 'Time to wait for the video to be generated in seconds',
				typeOptions: {
					minValue: 5,
					maxValue: 7200,
				},
			},
			{
				displayName: 'Output Field Name',
				name: 'fileName',
				type: 'string',
				default: 'data',
				hint: 'The name of the output field to put the binary file data in',
			},
		],
	},
];

const displayOptions = {
	show: {
		operation: ['generate'],
		resource: ['video'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const model = this.getNodeParameter('modelId', i, '', { extractValue: true }) as string;
	const prompt = this.getNodeParameter('prompt', i) as string;
	const seconds = this.getNodeParameter('seconds', i) as number;
	const size = this.getNodeParameter('size', i) as string;
	const options = this.getNodeParameter('options', i, {});
	const waitSeconds = (options.waitTime as number) || 300;

	const formData = new FormData();

	formData.append('model', model);
	formData.append('prompt', prompt);
	formData.append('seconds', seconds.toString());
	formData.append('size', size);

	if (options.binaryPropertyNameReference) {
		const { fileContent, contentType, filename } = await getBinaryDataFile(
			this,
			i,
			options.binaryPropertyNameReference as string,
		);
		const buffer = await this.helpers.binaryToBuffer(fileContent);
		formData.append('input_reference', buffer, {
			filename,
			contentType,
		});
	}

	const response = (await apiRequest.call(this, 'POST', '/videos', {
		option: { formData },
		headers: formData.getHeaders(),
	})) as VideoJob;

	const finalResponse = await pollUntilAvailable(
		this,
		async () => {
			return (await apiRequest.call(this, 'GET', `/videos/${response.id}`)) as VideoJob;
		},
		(response) => {
			if (response.error) {
				throw new NodeOperationError(this.getNode(), 'Error generating video', {
					description: response.error.message,
					itemIndex: i,
				});
			}
			return response.status === 'completed';
		},
		waitSeconds,
		10,
	);

	const contentResponse = await apiRequest.call(
		this,
		'GET',
		`/videos/${finalResponse.id}/content`,
		{
			option: {
				useStream: true,
				resolveWithFullResponse: true,
				json: false,
				encoding: null,
			},
		},
	);

	const mimeType = contentResponse.headers['content-type'];

	const binaryData = await this.helpers.prepareBinaryData(
		contentResponse.body,
		(options.fileName as string) || 'data',
		mimeType,
	);

	return [
		{
			json: Object.assign({}, binaryData, {
				data: undefined,
			}),
			binary: {
				data: binaryData,
			},
			pairedItem: { item: i },
		},
	];
}
