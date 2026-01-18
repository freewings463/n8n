"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/SolarWindsIpamApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:SolarWindsIpamApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/SolarWindsIpamApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/SolarWindsIpamApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class SolarWindsIpamApi implements ICredentialType {
	name = 'solarWindsIpamApi';

	displayName = 'SolarWinds IPAM';

	documentationUrl = 'solarwindsipam';

	icon = {
		light: 'file:icons/SolarWindsIpam.svg',
		dark: 'file:icons/SolarWindsIpam.svg',
	} as const;

	httpRequestNode = {
		name: 'SolarWinds IPAM',
		docsUrl: 'https://www.solarwinds.com/ip-address-manager',
		apiBaseUrlPlaceholder: 'https://your-ipam-server',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'Base URL',
			name: 'url',
			required: true,
			type: 'string',
			default: '',
			placeholder: 'https://your-ipam-server',
			description: 'The base URL of your SolarWinds IPAM server.',
		},
		{
			displayName: 'Username',
			name: 'username',
			required: true,
			type: 'string',
			default: '',
			description: 'The username for SolarWinds IPAM API.',
		},
		{
			displayName: 'Password',
			name: 'password',
			required: true,
			type: 'string',
			typeOptions: { password: true },
			default: '',
			description: 'The password for SolarWinds IPAM API.',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			auth: {
				username: '={{$credentials.username}}',
				password: '={{$credentials.password}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.url}}'.replace(/\/$/, ''),
			url: '/SolarWinds/InformationService/v3/Json/Query',
			method: 'GET',
			qs: {
				query: 'SELECT TOP 1 AccountID FROM IPAM.AccountRoles',
			},
			skipSslCertificateValidation: true,
		},
		rules: [
			{
				type: 'responseCode',
				properties: {
					value: 403,
					message: 'Connection failed: Invalid credentials or unreachable server',
				},
			},
		],
	};
}
