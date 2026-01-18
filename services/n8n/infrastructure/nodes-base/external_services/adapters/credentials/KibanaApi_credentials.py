"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/KibanaApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:KibanaApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/KibanaApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/KibanaApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
	Icon,
} from 'n8n-workflow';

export class KibanaApi implements ICredentialType {
	name = 'kibanaApi';

	displayName = 'Kibana API';

	documentationUrl = 'kibana';

	icon: Icon = 'file:icons/Kibana.svg';

	httpRequestNode = {
		name: 'Kibana',
		docsUrl: 'https://www.elastic.co/guide/en/kibana/current/api.html',
		apiBaseUrl: '',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'URL',
			name: 'url',
			type: 'string',
			required: true,
			default: '',
			placeholder: 'http://localhost:5601',
		},
		{
			displayName: 'Username',
			name: 'username',
			type: 'string',
			required: true,
			default: '',
		},
		{
			displayName: 'Password',
			name: 'password',
			type: 'string',
			typeOptions: { password: true },
			required: true,
			default: '',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				'kbn-xsrf': true,
			},
			auth: {
				username: '={{$credentials.username}}',
				password: '={{$credentials.password}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.url}}',
			url: '/api/features',
		},
	};
}
