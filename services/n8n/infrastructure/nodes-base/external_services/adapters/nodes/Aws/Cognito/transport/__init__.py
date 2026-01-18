"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/Cognito/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/Cognito 的入口。导入/依赖:外部:无；内部:无；本地:../aws/types。导出:无。关键函数/方法:awsApiRequest、awsApiRequestAllItems、response、items。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/Cognito/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/Cognito/transport/__init__.py

import type {
	ILoadOptionsFunctions,
	IPollFunctions,
	IHttpRequestOptions,
	IExecuteSingleFunctions,
	IDataObject,
	IHttpRequestMethods,
} from 'n8n-workflow';
import type { AwsIamCredentialsType } from '../../../../credentials/common/aws/types';

export async function awsApiRequest(
	this: ILoadOptionsFunctions | IPollFunctions | IExecuteSingleFunctions,
	method: IHttpRequestMethods,
	action: string,
	body: string,
): Promise<any> {
	const credentialsType = 'aws';
	const credentials = await this.getCredentials<AwsIamCredentialsType>(credentialsType);

	const requestOptions: IHttpRequestOptions = {
		url: '',
		method,
		body,
		headers: {
			'Content-Type': 'application/x-amz-json-1.1',
			'X-Amz-Target': `AWSCognitoIdentityProviderService.${action}`,
		},
		qs: {
			service: 'cognito-idp',
			_region: credentials.region,
		},
	};

	return await this.helpers.httpRequestWithAuthentication.call(
		this,
		credentialsType,
		requestOptions,
	);
}

export async function awsApiRequestAllItems(
	this: ILoadOptionsFunctions | IPollFunctions | IExecuteSingleFunctions,
	method: IHttpRequestMethods,
	action: string,
	body: IDataObject,
	propertyName: string,
): Promise<IDataObject[]> {
	const returnData: IDataObject[] = [];
	let nextToken: string | undefined;

	do {
		const requestBody: IDataObject = {
			...body,
			...(nextToken ? { NextToken: nextToken } : {}),
		};

		const response = (await awsApiRequest.call(
			this,
			method,
			action,
			JSON.stringify(requestBody),
		)) as IDataObject;

		const items = (response[propertyName] ?? []) as IDataObject[];
		returnData.push(...items);

		nextToken = response.NextToken as string | undefined;
	} while (nextToken);

	return returnData;
}
