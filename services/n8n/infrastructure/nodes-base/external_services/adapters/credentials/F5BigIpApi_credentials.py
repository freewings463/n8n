"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/F5BigIpApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:F5BigIpApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/F5BigIpApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/F5BigIpApi_credentials.py

import type { IAuthenticateGeneric, ICredentialType, INodeProperties, Icon } from 'n8n-workflow';

export class F5BigIpApi implements ICredentialType {
	name = 'f5BigIpApi';

	displayName = 'F5 Big-IP API';

	documentationUrl = 'f5bigip';

	icon: Icon = 'file:icons/F5.svg';

	httpRequestNode = {
		name: 'F5 Big-IP',
		docsUrl: 'https://clouddocs.f5.com/api/',
		apiBaseUrl: '',
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
}
