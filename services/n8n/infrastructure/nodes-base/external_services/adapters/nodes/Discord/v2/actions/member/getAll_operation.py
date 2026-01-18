"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discord/v2/actions/member/getAll.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discord/v2 的节点。导入/依赖:外部:无；内部:无；本地:../utils/descriptions、../utils/utilities、../helpers/utils、../../transport 等1项。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discord/v2/actions/member/getAll.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discord/v2/actions/member/getAll_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { returnAllOrLimit } from '../../../../../utils/descriptions';
import { updateDisplayOptions } from '../../../../../utils/utilities';
import { createSimplifyFunction, parseDiscordError, prepareErrorData } from '../../helpers/utils';
import { discordApiRequest } from '../../transport';
import { simplifyBoolean } from '../common.description';

const properties: INodeProperties[] = [
	...returnAllOrLimit,
	{
		displayName: 'After',
		name: 'after',
		type: 'string',
		default: '',
		placeholder: 'e.g. 786953432728469534',
		description: 'The ID of the user after which to return the members',
	},
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
		resource: ['member'],
		operation: ['getAll'],
	},
	hide: {
		authentication: ['webhook'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	guildId: string,
): Promise<INodeExecutionData[]> {
	const returnData: INodeExecutionData[] = [];

	const returnAll = this.getNodeParameter('returnAll', 0, false);
	const after = this.getNodeParameter('after', 0);

	const qs: IDataObject = {};

	if (!returnAll) {
		const limit = this.getNodeParameter('limit', 0);
		qs.limit = limit;
	}

	if (after) {
		qs.after = after;
	}

	let response: IDataObject[] = [];

	try {
		if (!returnAll) {
			const limit = this.getNodeParameter('limit', 0);
			qs.limit = limit;
			response = await discordApiRequest.call(
				this,
				'GET',
				`/guilds/${guildId}/members`,
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
					`/guilds/${guildId}/members`,
					undefined,
					qs,
				);
				if (!responseData?.length) break;
				qs.after = responseData[responseData.length - 1].user.id;
				response.push(...responseData);
			} while (responseData.length);
		}

		const simplify = this.getNodeParameter('options.simplify', 0, false) as boolean;

		if (simplify) {
			const simplifyResponse = createSimplifyFunction(['user', 'roles', 'permissions']);

			response = response.map(simplifyResponse);
		}

		const executionData = this.helpers.constructExecutionMetaData(
			this.helpers.returnJsonArray(response),
			{ itemData: { item: 0 } },
		);

		returnData.push(...executionData);
	} catch (error) {
		const err = parseDiscordError.call(this, error);

		if (this.continueOnFail()) {
			returnData.push(...prepareErrorData.call(this, err, 0));
		}

		throw err;
	}

	return returnData;
}
