"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/SalesforceJwtApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的JWT凭证。导入/依赖:外部:axios、jsonwebtoken、moment-timezone；内部:无；本地:无。导出:SalesforceJwtApi。关键函数/方法:authenticate。用于声明 n8n JWT鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/SalesforceJwtApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/SalesforceJwtApi_credentials.py

import type { AxiosRequestConfig } from 'axios';
import axios from 'axios';
import jwt from 'jsonwebtoken';
import moment from 'moment-timezone';
import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class SalesforceJwtApi implements ICredentialType {
	name = 'salesforceJwtApi';

	displayName = 'Salesforce JWT API';

	documentationUrl = 'salesforce';

	properties: INodeProperties[] = [
		{
			displayName: 'Environment Type',
			name: 'environment',
			type: 'options',
			options: [
				{
					name: 'Production',
					value: 'production',
				},
				{
					name: 'Sandbox',
					value: 'sandbox',
				},
			],
			default: 'production',
		},
		{
			displayName: 'Client ID',
			name: 'clientId',
			type: 'string',
			default: '',
			required: true,
			description: 'Consumer Key from Salesforce Connected App',
		},
		{
			displayName: 'Username',
			name: 'username',
			type: 'string',
			default: '',
			required: true,
		},
		{
			displayName: 'Private Key',
			name: 'privateKey',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
			required: true,
			description:
				'Use the multiline editor. Make sure it is in standard PEM key format:<br />-----BEGIN PRIVATE KEY-----<br />KEY DATA GOES HERE<br />-----END PRIVATE KEY-----',
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		const now = moment().unix();
		const authUrl =
			credentials.environment === 'sandbox'
				? 'https://test.salesforce.com'
				: 'https://login.salesforce.com';
		const signature = jwt.sign(
			{
				iss: credentials.clientId as string,
				sub: credentials.username as string,
				aud: authUrl,
				exp: now + 3 * 60,
			},
			credentials.privateKey as string,
			{
				algorithm: 'RS256',
				header: {
					alg: 'RS256',
				},
			},
		);

		const axiosRequestConfig: AxiosRequestConfig = {
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			},
			method: 'POST',
			data: new URLSearchParams({
				grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
				assertion: signature,
			}).toString(),
			url: `${authUrl}/services/oauth2/token`,
			responseType: 'json',
		};
		const result = await axios(axiosRequestConfig);
		const { access_token } = result.data as { access_token: string };

		return {
			...requestOptions,
			headers: {
				...requestOptions.headers,
				Authorization: `Bearer ${access_token}`,
			},
		};
	}

	test: ICredentialTestRequest = {
		request: {
			baseURL:
				'={{$credentials?.environment === "sandbox" ? "https://test.salesforce.com" : "https://login.salesforce.com"}}',
			url: '/services/oauth2/userinfo',
			method: 'GET',
		},
	};
}
