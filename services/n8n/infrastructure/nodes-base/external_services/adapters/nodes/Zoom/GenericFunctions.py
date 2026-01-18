"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Zoom/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Zoom 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:zoomApiRequest、wait、setTimeout、resolve、zoomApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Zoom/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Zoom/GenericFunctions.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function zoomApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: object = {},
	query: IDataObject = {},
	headers: IDataObject | undefined = undefined,
	option: IDataObject = {},
) {
	const authenticationMethod = this.getNodeParameter('authentication', 0, 'accessToken') as string;

	let options: IRequestOptions = {
		method,
		headers: headers || {
			'Content-Type': 'application/json',
		},
		body,
		qs: query,
		uri: `https://api.zoom.us/v2${resource}`,
		json: true,
	};
	options = Object.assign({}, options, option);
	if (Object.keys(body).length === 0) {
		delete options.body;
	}
	if (Object.keys(query).length === 0) {
		delete options.qs;
	}

	try {
		if (authenticationMethod === 'accessToken') {
			return await this.helpers.requestWithAuthentication.call(this, 'zoomApi', options);
		} else {
			return await this.helpers.requestOAuth2.call(this, 'zoomOAuth2Api', options);
		}
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

async function wait() {
	return await new Promise((resolve, _reject) => {
		setTimeout(() => {
			resolve(true);
		}, 1000);
	});
}

export async function zoomApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	query: IDataObject = {},
) {
	const returnData: IDataObject[] = [];
	let responseData;
	query.page_number = 0;
	do {
		responseData = await zoomApiRequest.call(this, method, endpoint, body, query);
		query.page_number++;
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
		// zoom free plan rate limit is 1 request/second
		// TODO just wait when the plan is free
		await wait();
	} while (responseData.page_count !== responseData.page_number);

	return returnData;
}
