"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SendGrid/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SendGrid 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:sendGridApiRequest、sendGridApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SendGrid/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SendGrid/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
} from 'n8n-workflow';

export async function sendGridApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	endpoint: string,
	method: IHttpRequestMethods,

	body: any = {},
	qs: IDataObject = {},
	option: IDataObject = {},
): Promise<any> {
	const host = 'api.sendgrid.com/v3';

	const options: IRequestOptions = {
		method,
		qs,
		body,
		uri: `https://${host}${endpoint}`,
		json: true,
	};

	if (Object.keys(body as IDataObject).length === 0) {
		delete options.body;
	}

	if (Object.keys(option).length !== 0) {
		Object.assign(options, option);
	}

	return await this.helpers.requestWithAuthentication.call(this, 'sendGridApi', options);
}

export async function sendGridApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	endpoint: string,
	method: IHttpRequestMethods,
	propertyName: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	let uri;

	do {
		responseData = await sendGridApiRequest.call(this, endpoint, method, body, query, uri); // possible bug, as function does not have uri parameter
		uri = responseData._metadata.next;
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
		const limit = query.limit as number | undefined;
		if (limit && returnData.length >= limit) {
			return returnData;
		}
	} while (responseData._metadata.next !== undefined);

	return returnData;
}
