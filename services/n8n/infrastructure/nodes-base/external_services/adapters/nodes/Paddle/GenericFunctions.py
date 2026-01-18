"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Paddle/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Paddle 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:validateJSON。关键函数/方法:paddleApiRequest、paddleApiRequestAllItems、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Paddle/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Paddle/GenericFunctions.py

import type {
	JsonObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IWebhookFunctions,
	IDataObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function paddleApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	endpoint: string,
	method: IHttpRequestMethods,

	body: any = {},
	_query?: IDataObject,
	_uri?: string,
): Promise<any> {
	const credentials = await this.getCredentials('paddleApi');
	const productionUrl = 'https://vendors.paddle.com/api';
	const sandboxUrl = 'https://sandbox-vendors.paddle.com/api';

	const isSandbox = credentials.sandbox;

	const options: IRequestOptions = {
		method,
		headers: {
			'content-type': 'application/json',
		},
		uri: `${isSandbox === true ? sandboxUrl : productionUrl}${endpoint}`,
		body,
		json: true,
	};

	body.vendor_id = credentials.vendorId;
	body.vendor_auth_code = credentials.vendorAuthCode;
	try {
		const response = await this.helpers.request(options);

		if (!response.success) {
			throw new NodeApiError(this.getNode(), response as JsonObject);
		}

		return response;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function paddleApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions,
	propertyName: string,
	endpoint: string,
	method: IHttpRequestMethods,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	body.results_per_page = 200;
	body.page = 1;

	do {
		responseData = await paddleApiRequest.call(this, endpoint, method, body, query);
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
		body.page++;
	} while (
		responseData[propertyName].length !== 0 &&
		responseData[propertyName].length === body.results_per_page
	);

	return returnData;
}

export function validateJSON(json: string | undefined): any {
	let result;
	try {
		result = JSON.parse(json!);
	} catch (exception) {
		result = undefined;
	}
	return result;
}
