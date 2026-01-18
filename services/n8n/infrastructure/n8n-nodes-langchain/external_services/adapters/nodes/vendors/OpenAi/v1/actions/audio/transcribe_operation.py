"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/audio/transcribe.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:form-data；内部:n8n-workflow；本地:../helpers/binary-data、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/audio/transcribe.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v1/actions/audio/transcribe_operation.py

import FormData from 'form-data';
import type { INodeProperties, IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { getBinaryDataFile } from '../../../helpers/binary-data';
import { apiRequest } from '../../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Input Data Field Name',
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		placeholder: 'e.g. data',
		hint: 'The name of the input field containing the binary file data to be processed',
		description:
			'Name of the binary property which contains the audio file in one of these formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm',
	},
	{
		displayName: 'Options',
		name: 'options',
		placeholder: 'Add Option',
		type: 'collection',
		default: {},
		options: [
			{
				displayName: 'Language of the Audio File',
				name: 'language',
				type: 'string',
				description:
					'The language of the input audio. Supplying the input language in <a href="https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes" target="_blank">ISO-639-1</a> format will improve accuracy and latency.',
				default: '',
			},
			{
				displayName: 'Output Randomness (Temperature)',
				name: 'temperature',
				type: 'number',
				default: 0,
				typeOptions: {
					minValue: 0,
					maxValue: 1,
					numberPrecision: 1,
				},
			},
		],
	},
];

const displayOptions = {
	show: {
		operation: ['transcribe'],
		resource: ['audio'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const model = 'whisper-1';
	const binaryPropertyName = this.getNodeParameter('binaryPropertyName', i);
	const options = this.getNodeParameter('options', i, {});

	const formData = new FormData();

	formData.append('model', model);

	if (options.language) {
		formData.append('language', options.language);
	}

	if (options.temperature) {
		formData.append('temperature', options.temperature.toString());
	}

	const { filename, contentType, fileContent } = await getBinaryDataFile(
		this,
		i,
		binaryPropertyName,
	);
	formData.append('file', fileContent, {
		filename,
		contentType,
	});

	const response = await apiRequest.call(this, 'POST', '/audio/transcriptions', {
		option: { formData },
		headers: formData.getHeaders(),
	});

	return [
		{
			json: response,
			pairedItem: { item: i },
		},
	];
}
