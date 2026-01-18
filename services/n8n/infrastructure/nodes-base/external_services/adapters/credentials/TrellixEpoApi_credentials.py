"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/TrellixEpoApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:TrellixEpoApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/TrellixEpoApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/TrellixEpoApi_credentials.py

import type { IAuthenticateGeneric, ICredentialType, INodeProperties, Icon } from 'n8n-workflow';

export class TrellixEpoApi implements ICredentialType {
	name = 'trellixEpoApi';

	displayName = 'Trellix (McAfee) ePolicy Orchestrator API';

	documentationUrl = 'trellixepo';

	icon: Icon = 'file:icons/Trellix.svg';

	httpRequestNode = {
		name: 'Trellix (McAfee) ePolicy Orchestrator',
		docsUrl: 'https://docs.trellix.com/en/bundle/epolicy-orchestrator-web-api-reference-guide',
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
