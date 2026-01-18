"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/audio/generate.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport。导出:description。关键函数/方法:execute、binaryPropertyOutput。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/audio/generate.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v2/actions/audio/generate_operation.py

import type {
	INodeProperties,
	IExecuteFunctions,
	IDataObject,
	INodeExecutionData,
} from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { apiRequest } from '../../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Model',
		name: 'model',
		type: 'options',
		default: 'tts-1',
		options: [
			{
				name: 'TTS-1',
				value: 'tts-1',
			},
			{
				name: 'TTS-1-HD',
				value: 'tts-1-hd',
			},
		],
	},
	{
		displayName: 'Text Input',
		name: 'input',
		type: 'string',
		placeholder: 'e.g. The quick brown fox jumped over the lazy dog',
		description: 'The text to generate audio for. The maximum length is 4096 characters.',
		default: '',
		typeOptions: {
			rows: 2,
		},
	},
	{
		displayName: 'Voice',
		name: 'voice',
		type: 'options',
		default: 'alloy',
		description: 'The voice to use when generating the audio',
		options: [
			{
				name: 'Alloy',
				value: 'alloy',
			},
			{
				name: 'Echo',
				value: 'echo',
			},
			{
				name: 'Fable',
				value: 'fable',
			},
			{
				name: 'Nova',
				value: 'nova',
			},
			{
				name: 'Onyx',
				value: 'onyx',
			},
			{
				name: 'Shimmer',
				value: 'shimmer',
			},
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
				displayName: 'Response Format',
				name: 'response_format',
				type: 'options',
				default: 'mp3',
				options: [
					{
						name: 'MP3',
						value: 'mp3',
					},
					{
						name: 'OPUS',
						value: 'opus',
					},
					{
						name: 'AAC',
						value: 'aac',
					},
					{
						name: 'FLAC',
						value: 'flac',
					},
				],
			},
			{
				displayName: 'Audio Speed',
				name: 'speed',
				type: 'number',
				default: 1,
				typeOptions: {
					minValue: 0.25,
					maxValue: 4,
					numberPrecision: 1,
				},
			},
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
		operation: ['generate'],
		resource: ['audio'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const model = this.getNodeParameter('model', i) as string;
	const input = this.getNodeParameter('input', i) as string;
	const voice = this.getNodeParameter('voice', i) as string;
	let response_format = 'mp3';
	let speed = 1;

	const options = this.getNodeParameter('options', i, {});

	if (options.response_format) {
		response_format = options.response_format as string;
	}

	if (options.speed) {
		speed = options.speed as number;
	}

	const body: IDataObject = {
		model,
		input,
		voice,
		response_format,
		speed,
	};

	const option = {
		useStream: true,
		returnFullResponse: true,
		encoding: 'arraybuffer',
		json: false,
	};

	const response = await apiRequest.call(this, 'POST', '/audio/speech', { body, option });

	const binaryData = await this.helpers.prepareBinaryData(
		response,
		`audio.${response_format}`,
		`audio/${response_format}`,
	);

	const binaryPropertyOutput = (options.binaryPropertyOutput as string) || 'data';

	const newItem: INodeExecutionData = {
		json: {
			...binaryData,
			data: undefined,
		},
		pairedItem: { item: i },
		binary: {
			[binaryPropertyOutput]: binaryData,
		},
	};

	return [newItem];
}
