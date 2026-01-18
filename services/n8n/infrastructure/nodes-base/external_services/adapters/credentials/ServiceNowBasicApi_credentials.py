"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/ServiceNowBasicApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:ServiceNowBasicApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/ServiceNowBasicApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/ServiceNowBasicApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class ServiceNowBasicApi implements ICredentialType {
	name = 'serviceNowBasicApi';

	extends = ['httpBasicAuth'];

	displayName = 'ServiceNow Basic Auth API';

	documentationUrl = 'servicenow';

	properties: INodeProperties[] = [
		{
			displayName: 'User',
			name: 'user',
			type: 'string',
			required: true,
			default: '',
		},
		{
			displayName: 'Password',
			name: 'password',
			type: 'string',
			required: true,
			typeOptions: {
				password: true,
			},
			default: '',
		},
		{
			displayName: 'Subdomain',
			name: 'subdomain',
			type: 'string',
			default: '',
			hint: 'The subdomain can be extracted from the URL. If the URL is: https://dev99890.service-now.com the subdomain is dev99890',
			required: true,
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			auth: {
				username: '={{$credentials.user}}',
				password: '={{$credentials.password}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '=https://{{$credentials?.subdomain}}.service-now.com',
			url: '/api/now/table/sys_user_role',
		},
	};
}
