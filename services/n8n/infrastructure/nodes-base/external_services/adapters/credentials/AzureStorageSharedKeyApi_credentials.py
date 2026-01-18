"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/AzureStorageSharedKeyApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:AzureStorageSharedKeyApi。关键函数/方法:authenticate、getCanonicalizedHeadersString、getCanonicalizedResourceString。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/AzureStorageSharedKeyApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/AzureStorageSharedKeyApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';
import { createHmac } from 'node:crypto';

import {
	getCanonicalizedHeadersString,
	getCanonicalizedResourceString,
	HeaderConstants,
	XMsVersion,
} from '../nodes/Microsoft/Storage/GenericFunctions';

export class AzureStorageSharedKeyApi implements ICredentialType {
	name = 'azureStorageSharedKeyApi';

	displayName = 'Azure Storage Shared Key API';

	documentationUrl = 'azurestorage';

	properties: INodeProperties[] = [
		{
			displayName: 'Account',
			name: 'account',
			description: 'Account name',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Key',
			name: 'key',
			description: 'Account key',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
		},
		{
			displayName: 'Base URL',
			name: 'baseUrl',
			type: 'hidden',
			default: '=https://{{ $self["account"] }}.blob.core.windows.net',
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		if (requestOptions.qs) {
			for (const [key, value] of Object.entries(requestOptions.qs)) {
				if (value === undefined) {
					delete requestOptions.qs[key];
				}
			}
		}
		if (requestOptions.headers) {
			for (const [key, value] of Object.entries(requestOptions.headers)) {
				if (value === undefined) {
					delete requestOptions.headers[key];
				}
			}
		}

		requestOptions.method ??= 'GET';
		requestOptions.headers ??= {};

		requestOptions.headers[HeaderConstants.X_MS_VERSION] ??= XMsVersion;
		requestOptions.headers[HeaderConstants.X_MS_DATE] ??= new Date().toUTCString();

		const stringToSign: string = [
			requestOptions.method.toUpperCase(),
			requestOptions.headers[HeaderConstants.CONTENT_LANGUAGE] ?? '',
			requestOptions.headers[HeaderConstants.CONTENT_ENCODING] ?? '',
			requestOptions.headers[HeaderConstants.CONTENT_LENGTH] ?? '',
			requestOptions.headers[HeaderConstants.CONTENT_MD5] ?? '',
			requestOptions.headers[HeaderConstants.CONTENT_TYPE] ?? '',
			requestOptions.headers[HeaderConstants.DATE] ?? '',
			requestOptions.headers[HeaderConstants.IF_MODIFIED_SINCE] ?? '',
			requestOptions.headers[HeaderConstants.IF_MATCH] ?? '',
			requestOptions.headers[HeaderConstants.IF_NONE_MATCH] ?? '',
			requestOptions.headers[HeaderConstants.IF_UNMODIFIED_SINCE] ?? '',
			requestOptions.headers[HeaderConstants.RANGE] ?? '',
			getCanonicalizedHeadersString(requestOptions) +
				getCanonicalizedResourceString(requestOptions, credentials),
		].join('\n');

		const signature: string = createHmac('sha256', Buffer.from(credentials.key as string, 'base64'))
			.update(stringToSign, 'utf8')
			.digest('base64');

		requestOptions.headers[HeaderConstants.AUTHORIZATION] =
			`SharedKey ${credentials.account as string}:${signature}`;

		return requestOptions;
	}

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.baseUrl}}',
			url: '/',
			headers: {
				'x-ms-date': '={{ new Date().toUTCString() }}',
				'x-ms-version': '2021-12-02',
			},
			qs: {
				comp: 'list',
			},
		},
	};
}
