"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/DynamoDB/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/DynamoDB 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./types、../GenericFunctions。导出:copyInputItem。关键函数/方法:awsApiRequest、statusCode、awsApiRequestAllItems、copyInputItem。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/DynamoDB/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/DynamoDB/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IWebhookFunctions,
	IHttpRequestOptions,
	INodeExecutionData,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { ApplicationError, deepCopy } from 'n8n-workflow';

import type { IRequestBody } from './types';
import { getAwsCredentials } from '../GenericFunctions';

export async function awsApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: object | IRequestBody,
	headers?: object,
): Promise<any> {
	const { credentials, credentialsType } = await getAwsCredentials(this);
	const requestOptions = {
		qs: {
			service,
			path,
		},
		method,
		body: JSON.stringify(body),
		url: '',
		headers,
		region: credentials?.region as string,
	} as IHttpRequestOptions;

	try {
		return JSON.parse(
			(await this.helpers.requestWithAuthentication.call(
				this,
				credentialsType,
				requestOptions,
			)) as string,
		);
	} catch (error) {
		const statusCode = (error.statusCode || error.cause?.statusCode) as number;
		let errorMessage =
			error.response?.body?.message || error.response?.body?.Message || error.message;

		if (statusCode === 403) {
			if (errorMessage === 'The security token included in the request is invalid.') {
				throw new ApplicationError('The AWS credentials are not valid!', { level: 'warning' });
			} else if (
				errorMessage.startsWith(
					'The request signature we calculated does not match the signature you provided',
				)
			) {
				throw new ApplicationError('The AWS credentials are not valid!', { level: 'warning' });
			}
		}

		if (error.cause?.error) {
			try {
				errorMessage = JSON.parse(error.cause?.error).message;
			} catch (ex) {}
		}

		throw new ApplicationError(`AWS error response [${statusCode}]: ${errorMessage}`, {
			level: 'warning',
		});
	}
}

export async function awsApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: IRequestBody,
	headers?: object,
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	do {
		const originalHeaders = Object.assign({}, headers); //The awsapirequest function adds the hmac signature to the headers, if we pass the modified headers back in on the next call it will fail with invalid signature
		responseData = await awsApiRequest.call(this, service, method, path, body, originalHeaders);
		if (responseData.LastEvaluatedKey) {
			body!.ExclusiveStartKey = responseData.LastEvaluatedKey;
		}
		returnData.push(...(responseData.Items as IDataObject[]));
	} while (responseData.LastEvaluatedKey !== undefined);

	return returnData;
}

export function copyInputItem(item: INodeExecutionData, properties: string[]): IDataObject {
	// Prepare the data to insert and copy it to be returned
	const newItem: IDataObject = {};
	for (const property of properties) {
		if (item.json[property] === undefined) {
			newItem[property] = null;
		} else {
			newItem[property] = deepCopy(item.json[property]);
		}
	}
	return newItem;
}
