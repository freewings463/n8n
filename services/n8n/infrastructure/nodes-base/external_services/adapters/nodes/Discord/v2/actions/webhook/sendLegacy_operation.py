"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discord/v2/actions/webhook/sendLegacy.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discord/v2 的Webhook节点。导入/依赖:外部:无；内部:无；本地:../utils/utilities、../../transport、../common.description。导出:description。关键函数/方法:execute、embeds、files。用于实现 n8n Webhook节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discord/v2/actions/webhook/sendLegacy.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discord/v2/actions/webhook/sendLegacy_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions } from '../../../../../utils/utilities';
import {
	parseDiscordError,
	prepareEmbeds,
	prepareErrorData,
	prepareMultiPartForm,
	prepareOptions,
} from '../../helpers/utils';
import { discordApiMultiPartRequest, discordApiRequest } from '../../transport';
import { embedsFixedCollection, filesFixedCollection } from '../common.description';

const properties: INodeProperties[] = [
	{
		displayName: 'Message',
		name: 'content',
		type: 'string',
		default: '',
		description: 'The content of the message (up to 2000 characters)',
		placeholder: 'e.g. My message',
		typeOptions: {
			rows: 2,
		},
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Avatar URL',
				name: 'avatar_url',
				type: 'string',
				default: '',
				description: 'Override the default avatar of the webhook',
				placeholder: 'e.g. https://example.com/image.png',
			},
			{
				displayName: 'Flags',
				name: 'flags',
				type: 'multiOptions',
				default: [],
				description:
					'Message flags. <a href="https://discord.com/developers/docs/resources/channel#message-object-message-flags" target="_blank">More info</a>.”.',
				options: [
					{
						name: 'Suppress Embeds',
						value: 'SUPPRESS_EMBEDS',
					},
					{
						name: 'Suppress Notifications',
						value: 'SUPPRESS_NOTIFICATIONS',
					},
				],
			},
			{
				displayName: 'Text-to-Speech (TTS)',
				name: 'tts',
				type: 'boolean',
				default: false,
				description: 'Whether to have a bot reading the message directly in the channel',
			},
			{
				displayName: 'Username',
				name: 'username',
				type: 'string',
				default: '',
				description: 'Override the default username of the webhook',
				placeholder: 'e.g. My Username',
			},
			{
				displayName: 'Wait',
				name: 'wait',
				type: 'boolean',
				default: false,
				description: 'Whether wait for the message to be created before returning its response',
			},
		],
	},
	embedsFixedCollection,
	filesFixedCollection,
];

const displayOptions = {
	show: {
		operation: ['sendLegacy'],
	},
	hide: {
		authentication: ['botToken', 'oAuth2'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions): Promise<INodeExecutionData[]> {
	const returnData: INodeExecutionData[] = [];
	const items = this.getInputData();

	for (let i = 0; i < items.length; i++) {
		const content = this.getNodeParameter('content', i) as string;
		const options = prepareOptions(this.getNodeParameter('options', i, {}));

		const embeds = (this.getNodeParameter('embeds', i, undefined) as IDataObject)
			?.values as IDataObject[];
		const files = (this.getNodeParameter('files', i, undefined) as IDataObject)
			?.values as IDataObject[];

		let qs: IDataObject | undefined = undefined;

		if (options.wait) {
			qs = {
				wait: options.wait,
			};

			delete options.wait;
		}

		const body: IDataObject = {
			content,
			...options,
		};

		if (embeds) {
			body.embeds = prepareEmbeds.call(this, embeds);
		}

		try {
			let response: IDataObject[] = [];

			if (files?.length) {
				const multiPartBody = await prepareMultiPartForm.call(this, files, body, i);

				response = await discordApiMultiPartRequest.call(this, 'POST', '', multiPartBody);
			} else {
				response = await discordApiRequest.call(this, 'POST', '', body, qs);
			}

			const executionData = this.helpers.constructExecutionMetaData(
				this.helpers.returnJsonArray(response),
				{ itemData: { item: i } },
			);

			returnData.push(...executionData);
		} catch (error) {
			const err = parseDiscordError.call(this, error, i);

			if (this.continueOnFail()) {
				returnData.push(...prepareErrorData.call(this, err, i));
				continue;
			}

			throw err;
		}
	}

	return returnData;
}
