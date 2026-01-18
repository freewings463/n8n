"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discord/v2/actions/message/getAll.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discord/v2 的节点。导入/依赖:外部:无；内部:无；本地:../utils/descriptions、../utils/utilities、../../transport、../common.description。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discord/v2/actions/message/getAll.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discord/v2/actions/message/getAll_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { returnAllOrLimit } from '../../../../../utils/descriptions';
import { updateDisplayOptions } from '../../../../../utils/utilities';
import {
	createSimplifyFunction,
	parseDiscordError,
	prepareErrorData,
	setupChannelGetter,
} from '../../helpers/utils';
import { discordApiRequest } from '../../transport';
import { channelRLC, simplifyBoolean } from '../common.description';

const properties: INodeProperties[] = [
	channelRLC,
	...returnAllOrLimit,
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [simplifyBoolean],
	},
];

const displayOptions = {
	show: {
		resource: ['message'],
		operation: ['getAll'],
	},
	hide: {
		authentication: ['webhook'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	_guildId: string,
	userGuilds: IDataObject[],
): Promise<INodeExecutionData[]> {
	const returnData: INodeExecutionData[] = [];
	const items = this.getInputData();
	const simplifyResponse = createSimplifyFunction([
		'id',
		'channel_id',
		'author',
		'content',
		'timestamp',
		'type',
	]);

	const getChannelId = await setupChannelGetter.call(this, userGuilds);

	for (let i = 0; i < items.length; i++) {
		try {
			const channelId = await getChannelId(i);

			const returnAll = this.getNodeParameter('returnAll', i, false);

			const qs: IDataObject = {};

			let response: IDataObject[] = [];

			if (!returnAll) {
				const limit = this.getNodeParameter('limit', 0);
				qs.limit = limit;
				response = await discordApiRequest.call(
					this,
					'GET',
					`/channels/${channelId}/messages`,
					undefined,
					qs,
				);
			} else {
				let responseData;
				qs.limit = 100;

				do {
					responseData = await discordApiRequest.call(
						this,
						'GET',
						`/channels/${channelId}/messages`,
						undefined,
						qs,
					);
					if (!responseData?.length) break;
					qs.before = responseData[responseData.length - 1].id;
					response.push(...responseData);
				} while (responseData.length);
			}

			const simplify = this.getNodeParameter('options.simplify', i, false) as boolean;

			if (simplify) {
				response = response.map(simplifyResponse);
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
