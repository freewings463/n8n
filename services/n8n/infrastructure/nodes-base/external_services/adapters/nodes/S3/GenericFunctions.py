"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/S3/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/S3 的节点。导入/依赖:外部:aws4、lodash/get、xml2js；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:get、queryToString、s3ApiRequest、sign、s3ApiRequestREST、s3ApiRequestSOAP、parseString、resolve、s3ApiRequestSOAPAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/S3/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/S3/GenericFunctions.py

import type { Request } from 'aws4';
import { sign } from 'aws4';
import get from 'lodash/get';
import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	IWebhookFunctions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';
import { URL } from 'url';
import { parseString } from 'xml2js';

function queryToString(params: IDataObject) {
	return Object.keys(params)
		.map((key) => key + '=' + (params[key] as string))
		.join('&');
}

export async function s3ApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	bucket: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string | Buffer,
	query: IDataObject = {},
	headers?: object,
	option: IDataObject = {},
	region?: string,
): Promise<any> {
	const credentials = await this.getCredentials('s3');

	if (!(credentials.endpoint as string).startsWith('http')) {
		throw new NodeOperationError(
			this.getNode(),
			'HTTP(S) Scheme is required in endpoint definition',
		);
	}

	const endpoint = new URL(credentials.endpoint as string);

	if (bucket) {
		if (credentials.forcePathStyle) {
			path = `/${bucket}${path}`;
		} else {
			endpoint.host = `${bucket}.${endpoint.host}`;
		}
	}

	endpoint.pathname = `${endpoint.pathname === '/' ? '' : endpoint.pathname}${path}`;

	// Sign AWS API request with the user credentials
	const signOpts = {
		headers: headers || {},
		region: region || credentials.region,
		host: endpoint.host,
		method,
		path: `${endpoint.pathname}?${queryToString(query).replace(/\+/g, '%2B')}`,
		service: 's3',
		body,
	} as Request;

	const securityHeaders = {
		accessKeyId: `${credentials.accessKeyId}`.trim(),
		secretAccessKey: `${credentials.secretAccessKey}`.trim(),
		sessionToken: credentials.temporaryCredentials
			? `${credentials.sessionToken}`.trim()
			: undefined,
	};

	sign(signOpts, securityHeaders);

	const options: IRequestOptions = {
		headers: signOpts.headers,
		method,
		qs: query,
		uri: endpoint.toString(),
		body: signOpts.body,
		rejectUnauthorized: !credentials.ignoreSSLIssues,
	};

	if (Object.keys(option).length !== 0) {
		Object.assign(options, option);
	}
	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function s3ApiRequestREST(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	bucket: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string,
	query: IDataObject = {},
	headers?: object,
	options: IDataObject = {},
	region?: string,
): Promise<any> {
	const response = await s3ApiRequest.call(
		this,
		bucket,
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
	} catch (error) {
		return response;
	}
}

export async function s3ApiRequestSOAP(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	bucket: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string | Buffer,
	query: IDataObject = {},
	headers?: object,
	option: IDataObject = {},
	region?: string,
): Promise<any> {
	const response = await s3ApiRequest.call(
		this,
		bucket,
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
	} catch (error) {
		return error;
	}
}

export async function s3ApiRequestSOAPAllItems(
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
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	do {
		responseData = await s3ApiRequestSOAP.call(
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
