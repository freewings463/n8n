"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MicrosoftAzureCosmosDbSharedKeyApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:MicrosoftAzureCosmosDbSharedKeyApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MicrosoftAzureCosmosDbSharedKeyApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MicrosoftAzureCosmosDbSharedKeyApi_credentials.py

import { createHmac } from 'crypto';
import type {
	ICredentialDataDecryptedObject,
	ICredentialType,
	ICredentialTestRequest,
	IHttpRequestOptions,
	INodeProperties,
	IRequestOptions,
} from 'n8n-workflow';
import { OperationalError } from 'n8n-workflow';

import {
	CURRENT_VERSION,
	HeaderConstants,
	RESOURCE_TYPES,
} from '../nodes/Microsoft/AzureCosmosDb/helpers/constants';

export class MicrosoftAzureCosmosDbSharedKeyApi implements ICredentialType {
	name = 'microsoftAzureCosmosDbSharedKeyApi';

	displayName = 'Microsoft Azure Cosmos DB API';

	documentationUrl = 'azurecosmosdb';

	properties: INodeProperties[] = [
		{
			displayName: 'Account',
			name: 'account',
			default: '',
			description: 'Account name',
			required: true,
			type: 'string',
		},
		{
			displayName: 'Key',
			name: 'key',
			default: '',
			description: 'Account key',
			required: true,
			type: 'string',
			typeOptions: {
				password: true,
			},
		},
		{
			displayName: 'Database',
			name: 'database',
			default: '',
			description: 'Database name',
			required: true,
			type: 'string',
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		const date = new Date().toUTCString();

		requestOptions.headers ??= {};
		requestOptions.headers = {
			...requestOptions.headers,
			'x-ms-date': date,
			'x-ms-version': CURRENT_VERSION,
			'Cache-Control': 'no-cache',
		};

		// HttpRequest node uses IRequestOptions.uri
		const url = new URL(
			(requestOptions as IRequestOptions).uri ?? requestOptions.baseURL + requestOptions.url,
		);

		const pathSegments = url.pathname.split('/').filter(Boolean);

		const foundResource = RESOURCE_TYPES.map((type) => ({
			type,
			index: pathSegments.lastIndexOf(type),
		}))
			.filter(({ index }) => index !== -1)
			.sort((a, b) => b.index - a.index)
			.shift();

		if (!foundResource) {
			throw new OperationalError('Unable to determine the resource type from the URL');
		}

		const { type, index } = foundResource;
		const resourceId =
			pathSegments[index + 1] !== undefined
				? `${pathSegments.slice(0, index).join('/')}/${type}/${pathSegments[index + 1]}`
				: pathSegments.slice(0, index).join('/');

		const key = Buffer.from(credentials.key as string, 'base64');
		const payload = `${(requestOptions.method ?? 'GET').toLowerCase()}\n${type.toLowerCase()}\n${resourceId}\n${date.toLowerCase()}\n\n`;
		const hmacSha256 = createHmac('sha256', key);
		const signature = hmacSha256.update(payload, 'utf8').digest('base64');

		requestOptions.headers[HeaderConstants.AUTHORIZATION] = encodeURIComponent(
			`type=master&ver=1.0&sig=${signature}`,
		);

		return requestOptions;
	}

	test: ICredentialTestRequest = {
		request: {
			baseURL:
				'=https://{{ $credentials.account }}.documents.azure.com/dbs/{{ $credentials.database }}',
			url: '/colls',
		},
	};
}
