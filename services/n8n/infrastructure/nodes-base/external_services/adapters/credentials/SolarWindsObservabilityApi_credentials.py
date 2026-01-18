"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/SolarWindsObservabilityApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:SolarWindsObservabilityApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/SolarWindsObservabilityApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/SolarWindsObservabilityApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class SolarWindsObservabilityApi implements ICredentialType {
	name = 'solarWindsObservabilityApi';

	displayName = 'SolarWinds Observability';

	documentationUrl = 'solarwindsobservability';

	icon = {
		light: 'file:icons/SolarWindsObservability.svg',
		dark: 'file:icons/SolarWindsObservability.svg',
	} as const;

	httpRequestNode = {
		name: 'SolarWinds Observability',
		docsUrl:
			'https://documentation.solarwinds.com/en/success_center/observability/content/api/api-swagger.htm',
		apiBaseUrlPlaceholder: 'https://api.xx-yy.cloud.solarwinds.com/',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'URL',
			name: 'url',
			required: true,
			type: 'string',
			default: '',
		},
		{
			displayName: 'API Token',
			name: 'apiToken',
			required: true,
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials.apiToken}}',
				'Content-Type': 'application/json-rpc',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.url}}'.replace(/\/$/, ''),
			url: '/v1/logs',
			method: 'GET',
		},
		rules: [
			{
				type: 'responseSuccessBody',
				properties: {
					key: 'error',
					value: 'invalid_auth',
					message: 'Invalid access token',
				},
			},
		],
	};
}
