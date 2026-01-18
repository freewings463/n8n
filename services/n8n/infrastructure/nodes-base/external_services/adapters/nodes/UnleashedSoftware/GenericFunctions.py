"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/UnleashedSoftware/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/UnleashedSoftware 的节点。导入/依赖:外部:qs；内部:n8n-workflow；本地:无。导出:convertNETDates。关键函数/方法:unleashedApiRequest、unleashedApiRequestAllItems、convertNETDates。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/UnleashedSoftware/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/UnleashedSoftware/GenericFunctions.py

import { createHmac } from 'crypto';
import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	JsonObject,
	IRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';
import qs from 'qs';

export async function unleashedApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	path: string,
	body: IDataObject = {},
	query: IDataObject = {},
	pageNumber?: number,
	headers?: object,
) {
	const paginatedPath = pageNumber ? `/${path}/${pageNumber}` : `/${path}`;

	const options: IRequestOptions = {
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
		method,
		qs: query,
		body,
		url: `https://api.unleashedsoftware.com/${paginatedPath}`,
		json: true,
	};

	if (Object.keys(body).length === 0) {
		delete options.body;
	}

	const credentials = await this.getCredentials('unleashedSoftwareApi');

	const signature = createHmac('sha256', credentials.apiKey as string)
		.update(qs.stringify(query))
		.digest('base64');

	options.headers = Object.assign({}, headers, {
		'api-auth-id': credentials.apiId,
		'api-auth-signature': signature,
	});

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function unleashedApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	query: IDataObject = {},
) {
	const returnData: IDataObject[] = [];
	let responseData;
	let pageNumber = 1;

	query.pageSize = 1000;

	do {
		responseData = await unleashedApiRequest.call(this, method, endpoint, body, query, pageNumber);
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
		pageNumber++;
	} while (
		(responseData.Pagination.PageNumber as number) <
		(responseData.Pagination.NumberOfPages as number)
	);
	return returnData;
}

//.NET code is serializing dates in the following format: "/Date(1586833770780)/"
//which is useless on JS side and could not treated as a date for other nodes
//so we need to convert all of the fields that has it.

export function convertNETDates(item: { [key: string]: any }) {
	Object.keys(item).forEach((path) => {
		const type = typeof item[path] as string;
		if (type === 'string') {
			const value = item[path] as string;
			const a = /\/Date\((\d*)\)\//.exec(value);
			if (a) {
				item[path] = new Date(+a[1]);
			}
		}
		if (type === 'object' && item[path]) {
			convertNETDates(item[path] as IDataObject);
		}
	});
}
