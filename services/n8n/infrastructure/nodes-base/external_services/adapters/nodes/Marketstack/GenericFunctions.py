"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Marketstack/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Marketstack 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:format、validateTimeOptions。关键函数/方法:marketstackApiRequest、marketstackApiRequestAllItems、format、validateTimeOptions。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Marketstack/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Marketstack/GenericFunctions.py

import type {
	IExecuteFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

export async function marketstackApiRequest(
	this: IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
) {
	const credentials = await this.getCredentials('marketstackApi');
	const protocol = credentials.useHttps ? 'https' : 'http'; // Free API does not support HTTPS

	const options: IRequestOptions = {
		method,
		uri: `${protocol}://api.marketstack.com/v1${endpoint}`,
		qs: {
			access_key: credentials.apiKey,
			...qs,
		},
		json: true,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function marketstackApiRequestAllItems(
	this: IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
) {
	const returnAll = this.getNodeParameter('returnAll', 0, false);
	const limit = this.getNodeParameter('limit', 0, 0);

	let responseData;
	const returnData: IDataObject[] = [];

	qs.offset = 0;

	do {
		responseData = await marketstackApiRequest.call(this, method, endpoint, body, qs);
		returnData.push(...(responseData.data as IDataObject[]));

		if (!returnAll && returnData.length > limit) {
			return returnData.slice(0, limit);
		}

		qs.offset += responseData.count;
	} while (responseData.total > returnData.length);

	return returnData;
}

export const format = (datetime?: string) => datetime?.split('T')[0];

export function validateTimeOptions(this: IExecuteFunctions, timeOptions: boolean[]) {
	if (timeOptions.every((o) => !o)) {
		throw new NodeOperationError(
			this.getNode(),
			'Please filter by latest, specific date or timeframe (start and end dates).',
		);
	}

	if (timeOptions.filter(Boolean).length > 1) {
		throw new NodeOperationError(
			this.getNode(),
			'Please filter by one of latest, specific date, or timeframe (start and end dates).',
		);
	}
}
