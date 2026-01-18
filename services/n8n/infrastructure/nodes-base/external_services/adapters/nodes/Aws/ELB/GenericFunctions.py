"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/ELB/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/ELB 的节点。导入/依赖:外部:lodash/get、xml2js；内部:n8n-workflow；本地:../GenericFunctions。导出:无。关键函数/方法:get、awsApiRequest、awsApiRequestREST、awsApiRequestSOAP、parseString、resolve、awsApiRequestSOAPAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/ELB/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/ELB/GenericFunctions.py

import get from 'lodash/get';
import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IWebhookFunctions,
	IHttpRequestOptions,
	JsonObject,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';
import { parseString } from 'xml2js';
import { getAwsCredentials } from '../GenericFunctions';

export async function awsApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string | Buffer,
	query: IDataObject = {},
	headers?: object,
	_option: IDataObject = {},
	_region?: string,
) {
	const { credentials, credentialsType } = await getAwsCredentials(this);

	const requestOptions = {
		qs: {
			...query,
			service,
			path,
		},
		headers,
		method,
		url: '',
		body,
		region: credentials?.region as string,
	} as IHttpRequestOptions;

	try {
		return await this.helpers.requestWithAuthentication.call(this, credentialsType, requestOptions);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function awsApiRequestREST(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string,
	query: IDataObject = {},
	headers?: object,
	options: IDataObject = {},
	region?: string,
) {
	const response = await awsApiRequest.call(
		this,
		service,
		method,
		path,
		body,
		query,
		headers,
		options,
		region,
	);
	try {
		return JSON.parse(response as string);
	} catch (e) {
		return response;
	}
}

export async function awsApiRequestSOAP(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string | Buffer,
	query: IDataObject = {},
	headers?: object,
	option: IDataObject = {},
	region?: string,
) {
	const response = await awsApiRequest.call(
		this,
		service,
		method,
		path,
		body,
		query,
		headers,
		option,
		region,
	);
	try {
		return await new Promise((resolve, reject) => {
			parseString(response as string, { explicitArray: false }, (err, data) => {
				if (err) {
					return reject(err);
				}
				resolve(data);
			});
		});
	} catch (e) {
		return e;
	}
}

export async function awsApiRequestSOAPAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	propertyName: string,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string,
	query: IDataObject = {},
	headers: IDataObject = {},
	option: IDataObject = {},
	region?: string,
) {
	const returnData: IDataObject[] = [];

	let responseData;

	const propertyNameArray = propertyName.split('.');

	do {
		responseData = await awsApiRequestSOAP.call(
			this,
			service,
			method,
			path,
			body,
			query,
			headers,
			option,
			region,
		);

		if (get(responseData, [propertyNameArray[0], propertyNameArray[1], 'NextMarker'])) {
			query.Marker = get(responseData, [propertyNameArray[0], propertyNameArray[1], 'NextMarker']);
		}
		if (get(responseData, propertyName)) {
			if (Array.isArray(get(responseData, propertyName))) {
				returnData.push.apply(returnData, get(responseData, propertyName) as IDataObject[]);
			} else {
				returnData.push(get(responseData, propertyName) as IDataObject);
			}
		}
	} while (
		get(responseData, [propertyNameArray[0], propertyNameArray[1], 'NextMarker']) !== undefined
	);

	return returnData;
}
