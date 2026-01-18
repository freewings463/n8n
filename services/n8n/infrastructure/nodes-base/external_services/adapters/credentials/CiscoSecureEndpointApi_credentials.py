"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/CiscoSecureEndpointApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:axios；内部:无；本地:无。导出:CiscoSecureEndpointApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/CiscoSecureEndpointApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/CiscoSecureEndpointApi_credentials.py

import axios from 'axios';
import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class CiscoSecureEndpointApi implements ICredentialType {
	name = 'ciscoSecureEndpointApi';

	displayName = 'Cisco Secure Endpoint (AMP) API';

	documentationUrl = 'ciscosecureendpoint';

	icon = { light: 'file:icons/Cisco.svg', dark: 'file:icons/Cisco.dark.svg' } as const;

	httpRequestNode = {
		name: 'Cisco Secure Endpoint',
		docsUrl: 'https://developer.cisco.com/docs/secure-endpoint/',
		apiBaseUrl: '',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'Region',
			name: 'region',
			type: 'options',
			options: [
				{
					name: 'Asia Pacific, Japan, and China',
					value: 'apjc.amp',
				},
				{
					name: 'Europe',
					value: 'eu.amp',
				},
				{
					name: 'North America',
					value: 'amp',
				},
			],
			default: 'amp',
		},
		{
			displayName: 'Client ID',
			name: 'clientId',
			type: 'string',
			default: '',
			required: true,
		},
		{
			displayName: 'Client Secret',
			name: 'clientSecret',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
			required: true,
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		const clientId = credentials.clientId as string;
		const clientSecret = credentials.clientSecret as string;
		const region = credentials.region as string;

		const secureXToken = await axios({
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
				Accept: 'application/json',
			},
			auth: {
				username: clientId,
				password: clientSecret,
			},
			method: 'POST',
			data: new URLSearchParams({
				grant_type: 'client_credentials',
			}).toString(),
			url: `https://visibility.${region}.cisco.com/iroh/oauth2/token`,
		});

		const secureEndpointToken = await axios({
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
				Accept: 'application/json',
				Authorization: `Bearer ${secureXToken.data.access_token}`,
			},
			method: 'POST',
			data: new URLSearchParams({
				grant_type: 'client_credentials',
			}).toString(),
			url: `https://api.${region}.cisco.com/v3/access_tokens`,
		});

		const requestOptionsWithAuth: IHttpRequestOptions = {
			...requestOptions,
			headers: {
				...requestOptions.headers,
				Authorization: `Bearer ${secureEndpointToken.data.access_token}`,
			},
		};

		return requestOptionsWithAuth;
	}

	test: ICredentialTestRequest = {
		request: {
			baseURL: '=https://api.{{$credentials.region}}.cisco.com',
			url: '/v3/organizations',
			qs: {
				size: 10,
			},
		},
	};
}
