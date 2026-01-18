"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws 的节点。导入/依赖:外部:xml2js；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:getAwsCredentials、awsApiRequest、awsApiRequestREST、awsApiRequestSOAP、parseXml、resolve。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/GenericFunctions.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IWebhookFunctions,
	IHttpRequestOptions,
	JsonObject,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';
import { parseString as parseXml } from 'xml2js';
import type {
	AwsAssumeRoleCredentialsType,
	AwsIamCredentialsType,
} from '../../credentials/common/aws/types';

export async function getAwsCredentials(
	context: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
) {
	let credentialsType: 'aws' | 'awsAssumeRole' = 'aws';

	try {
		const authentication = context.getNodeParameter('authentication', 0) as 'iam' | 'assumeRole';

		if (authentication === 'assumeRole') {
			credentialsType = 'awsAssumeRole';
		}
	} catch (error) {
		context.logger.warn('Could not get authentication type');
	}

	const credentials: AwsIamCredentialsType | AwsAssumeRoleCredentialsType =
		await context.getCredentials(credentialsType);

	return { credentials, credentialsType };
}

export async function awsApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string,
	headers?: object,
): Promise<any> {
	const { credentials, credentialsType } = await getAwsCredentials(this);
	const requestOptions = {
		qs: {
			service,
			path,
		},
		method,
		body: service === 'lambda' ? body : JSON.stringify(body),
		url: '',
		headers,
		region: credentials?.region as string,
	} as IHttpRequestOptions;

	try {
		return await this.helpers.requestWithAuthentication.call(this, credentialsType, requestOptions);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject, { parseXml: true });
	}
}

export async function awsApiRequestREST(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string,
	headers?: object,
): Promise<any> {
	const response = await awsApiRequest.call(this, service, method, path, body, headers);
	try {
		return JSON.parse(response as string);
	} catch (error) {
		return response;
	}
}

export async function awsApiRequestSOAP(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	service: string,
	method: IHttpRequestMethods,
	path: string,
	body?: string,
	headers?: object,
): Promise<any> {
	const response = await awsApiRequest.call(this, service, method, path, body, headers);
	try {
		return await new Promise((resolve, reject) => {
			parseXml(response as string, { explicitArray: false }, (err, data) => {
				if (err) {
					return reject(err);
				}
				resolve(data);
			});
		});
	} catch (error) {
		return response;
	}
}
