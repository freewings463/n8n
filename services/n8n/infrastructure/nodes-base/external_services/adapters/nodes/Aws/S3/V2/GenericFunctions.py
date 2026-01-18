"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/S3/V2/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/S3 的节点。导入/依赖:外部:lodash/get、xml2js；内部:无；本地:../../GenericFunctions。导出:无。关键函数/方法:get、awsApiRequest、awsApiRequestREST、parseString、resolve、awsApiRequestRESTAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/S3/V2/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/S3/V2/GenericFunctions.py

import get from 'lodash/get';
import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IWebhookFunctions,
	IHttpRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { parseString } from 'xml2js';
import { getAwsCredentials } from '../../GenericFunctions';

export async function awsApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string | Buffer | any,
	query: IDataObject = {},
	headers?: object,
	option: IDataObject = {},
	_region?: string,
): Promise<any> {
	const requestOptions = {
		qs: {
			...query,
			service,
			path,
			query,
			_region,
		},
		method,
		body,
		url: '',
		headers,
	} as IHttpRequestOptions;

	if (Object.keys(option).length !== 0) {
		Object.assign(requestOptions, option);
	}
	const { credentialsType } = await getAwsCredentials(this);

	return await this.helpers.requestWithAuthentication.call(this, credentialsType, requestOptions);
}

export async function awsApiRequestREST(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string | Buffer | any,
	query: IDataObject = {},
	headers?: object,
	options: IDataObject = {},
	region?: string,
): Promise<any> {
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
		if (response.includes('<?xml version="1.0" encoding="UTF-8"?>')) {
			return await new Promise((resolve, reject) => {
				parseString(response as string, { explicitArray: false }, (err, data) => {
					if (err) {
						return reject(err);
					}
					resolve(data);
				});
			});
		}
		return JSON.parse(response as string);
	} catch (error) {
		return response;
	}
}

export async function awsApiRequestRESTAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string,
	query: IDataObject = {},
	headers?: object,
	option: IDataObject = {},
	region?: string,
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;
	do {
		responseData = await awsApiRequestREST.call(
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
		//https://forums.aws.amazon.com/thread.jspa?threadID=55746
		if (get(responseData, [propertyName.split('.')[0], 'NextContinuationToken'])) {
			query['continuation-token'] = get(responseData, [
				propertyName.split('.')[0],
				'NextContinuationToken',
			]);
		}
		if (get(responseData, propertyName)) {
			if (Array.isArray(get(responseData, propertyName))) {
				returnData.push.apply(returnData, get(responseData, propertyName) as IDataObject[]);
			} else {
				returnData.push(get(responseData, propertyName) as IDataObject);
			}
		}
		const limit = query.limit as number | undefined;
		if (limit && limit <= returnData.length) {
			return returnData;
		}
	} while (
		get(responseData, [propertyName.split('.')[0], 'IsTruncated']) !== undefined &&
		get(responseData, [propertyName.split('.')[0], 'IsTruncated']) !== 'false'
	);
	return returnData;
}
