"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Autopilot/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Autopilot 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:autopilotApiRequest、autopilotApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Autopilot/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Autopilot/GenericFunctions.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	IHookFunctions,
	IWebhookFunctions,
	JsonObject,
	IRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function autopilotApiRequest(
	this: IExecuteFunctions | IWebhookFunctions | IHookFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: any = {},
	query: IDataObject = {},
	uri?: string,
	_option: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials<{ apiKey: string }>('autopilotApi');

	const endpoint = 'https://api2.autopilothq.com/v1';

	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
			autopilotapikey: credentials.apiKey,
		},
		method,
		body,
		qs: query,
		uri: uri || `${endpoint}${resource}`,
		json: true,
	};
	if (!Object.keys(body as IDataObject).length) {
		delete options.body;
	}
	if (!Object.keys(query).length) {
		delete options.qs;
	}

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function autopilotApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];
	const returnAll = this.getNodeParameter('returnAll', 0, false) as boolean;

	const base = endpoint;

	let responseData;
	do {
		responseData = await autopilotApiRequest.call(this, method, endpoint, body, query);
		endpoint = `${base}/${responseData.bookmark}`;
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
		const limit = query.limit as number | undefined;
		if (limit && returnData.length >= limit && !returnAll) {
			return returnData;
		}
	} while (responseData.bookmark !== undefined);
	return returnData;
}
