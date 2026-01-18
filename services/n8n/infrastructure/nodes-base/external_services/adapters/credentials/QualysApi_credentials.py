"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/QualysApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:QualysApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/QualysApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/QualysApi_credentials.py

import type { IAuthenticateGeneric, ICredentialType, INodeProperties } from 'n8n-workflow';

export class QualysApi implements ICredentialType {
	name = 'qualysApi';

	displayName = 'Qualys API';

	icon = 'file:icons/Qualys.svg' as const;

	documentationUrl = 'qualys';

	httpRequestNode = {
		name: 'Qualys',
		docsUrl: 'https://qualysguard.qg2.apps.qualys.com/qwebhelp/fo_portal/api_doc/index.htm',
		apiBaseUrl: 'https://qualysapi.qualys.com/api/',
	};

	properties: INodeProperties[] = [
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
			displayName: 'Requested With',
			name: 'requestedWith',
			type: 'string',
			default: 'n8n application',
			description: 'User description, like a user agent',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				'X-Requested-With': '={{$credentials.requestedWith}}',
			},
			auth: {
				username: '={{$credentials.username}}',
				password: '={{$credentials.password}}',
			},
		},
	};

	// test: ICredentialTestRequest = {
	// 	request: {
	// 		baseURL: 'https://qualysapi.qualys.com',
	// 		url: '/api/2.0/fo/asset/host/?action=list',
	// 	},
	// };
}
