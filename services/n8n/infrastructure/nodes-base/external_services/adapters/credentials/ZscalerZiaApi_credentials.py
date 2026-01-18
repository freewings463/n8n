"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/ZscalerZiaApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:ZscalerZiaApi。关键函数/方法:preAuthentication、url、obfuscate、cookie。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/ZscalerZiaApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/ZscalerZiaApi_credentials.py

import { ApplicationError } from '@n8n/errors';
import type {
	IAuthenticateGeneric,
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestHelper,
	INodeProperties,
	Icon,
} from 'n8n-workflow';

export class ZscalerZiaApi implements ICredentialType {
	name = 'zscalerZiaApi';

	displayName = 'Zscaler ZIA API';

	documentationUrl = 'zscalerzia';

	icon: Icon = 'file:icons/Zscaler.svg';

	httpRequestNode = {
		name: 'Zscaler ZIA',
		docsUrl: 'https://help.zscaler.com/zia/getting-started-zia-api',
		apiBaseUrl: '',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'Cookie',
			name: 'cookie',
			type: 'hidden',
			typeOptions: {
				expirable: true,
			},
			default: '',
		},
		{
			displayName: 'Base URL',
			name: 'baseUrl',
			type: 'string',
			default: '',
			placeholder: 'e.g. zsapi.zscalerthree.net',
			required: true,
		},
		{
			displayName: 'Username',
			name: 'username',
			type: 'string',
			default: '',
			required: true,
		},
		{
			displayName: 'Password',
			name: 'password',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: true,
		},
		{
			displayName: 'Api Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
			required: true,
		},
	];

	async preAuthentication(this: IHttpRequestHelper, credentials: ICredentialDataDecryptedObject) {
		const { baseUrl, username, password, apiKey } = credentials;

		const url = (baseUrl as string).endsWith('/')
			? (baseUrl as string).slice(0, -1)
			: (baseUrl as string);

		const now = Date.now().toString();

		const obfuscate = (key: string, timestamp: string) => {
			const high = timestamp.substring(timestamp.length - 6);
			let low = (parseInt(high) >> 1).toString();

			let obfuscatedApiKey = '';
			while (low.length < 6) {
				low = '0' + low;
			}

			for (let i = 0; i < high.length; i++) {
				obfuscatedApiKey += key.charAt(parseInt(high.charAt(i)));
			}
			for (let j = 0; j < low.length; j++) {
				obfuscatedApiKey += key.charAt(parseInt(low.charAt(j)) + 2);
			}

			return obfuscatedApiKey;
		};

		const response = await this.helpers.httpRequest({
			method: 'POST',
			baseURL: `https://${url}`,
			url: '/api/v1/authenticatedSession',
			headers: {
				'Content-Type': 'application/json',
				'Cache-Control': 'no-cache',
			},
			body: {
				apiKey: obfuscate(apiKey as string, now),
				username,
				password,
				timestamp: now,
			},
			returnFullResponse: true,
		});

		const headers = response.headers;

		const cookie = (headers['set-cookie'] as string[])
			?.find((entrt) => entrt.includes('JSESSIONID'))
			?.split(';')
			?.find((entry) => entry.includes('JSESSIONID'));

		if (!cookie) {
			throw new ApplicationError('No cookie returned. Please check your credentials.', {
				level: 'warning',
			});
		}

		return { cookie };
	}

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Cookie: '={{$credentials.cookie}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			url: '=https://{{$credentials.baseUrl}}/api/v1/authSettings/exemptedUrls',
		},
	};
}
