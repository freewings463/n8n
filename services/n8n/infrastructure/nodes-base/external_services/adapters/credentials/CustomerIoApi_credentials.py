"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/CustomerIoApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:CustomerIoApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/CustomerIoApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/CustomerIoApi_credentials.py

import { ApplicationError } from '@n8n/errors';
import type {
	ICredentialDataDecryptedObject,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class CustomerIoApi implements ICredentialType {
	name = 'customerIoApi';

	displayName = 'Customer.io API';

	documentationUrl = 'customerio';

	properties: INodeProperties[] = [
		{
			displayName: 'Tracking API Key',
			name: 'trackingApiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			description: 'Required for tracking API',
			required: true,
		},
		{
			displayName: 'Region',
			name: 'region',
			type: 'options',
			options: [
				{
					name: 'EU region',
					value: 'track-eu.customer.io',
				},
				{
					name: 'Global region',
					value: 'track.customer.io',
				},
			],
			default: 'track.customer.io',
			description: 'Should be set based on your account region',
			hint: 'The region will be omitted when being used with the HTTP node',
			required: true,
		},
		{
			displayName: 'Tracking Site ID',
			name: 'trackingSiteId',
			type: 'string',
			default: '',
			description: 'Required for tracking API',
		},
		{
			displayName: 'App API Key',
			name: 'appApiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			description: 'Required for App API',
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		// @ts-ignore
		const url = new URL(requestOptions.url ? requestOptions.url : requestOptions.uri);
		if (
			url.hostname === 'track.customer.io' ||
			url.hostname === 'track-eu.customer.io' ||
			url.hostname === 'api.customer.io' ||
			url.hostname === 'api-eu.customer.io'
		) {
			const basicAuthKey = Buffer.from(
				`${credentials.trackingSiteId}:${credentials.trackingApiKey}`,
			).toString('base64');
			// @ts-ignore
			Object.assign(requestOptions.headers, { Authorization: `Basic ${basicAuthKey}` });
		} else if (
			url.hostname === 'beta-api.customer.io' ||
			url.hostname === 'beta-api-eu.customer.io'
		) {
			// @ts-ignore
			Object.assign(requestOptions.headers, {
				Authorization: `Bearer ${credentials.appApiKey as string}`,
			});
		} else {
			throw new ApplicationError('Unknown way of authenticating', { level: 'warning' });
		}

		return requestOptions;
	}
}
