"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/shared/credentials/bearer.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/shared 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:ExampleApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/shared/credentials/bearer.credentials.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/shared/credentials/bearer_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class ExampleApi implements ICredentialType {
	name = 'exampleApi';

	displayName = 'Example API';

	// Link to your community node's README
	documentationUrl = 'https://github.com/org/repo?tab=readme-ov-file#credentials';

	properties: INodeProperties[] = [
		{
			displayName: 'Access Token',
			name: 'accessToken',
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
				Authorization: '=Bearer {{$credentials.accessToken}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: 'https://api.example.com/v2',
			url: '/v1/user',
		},
	};
}
