"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/shared/credentials/oauth2AuthorizationCode.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/shared 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ExampleOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/shared/credentials/oauth2AuthorizationCode.credentials.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/shared/credentials/oauth2AuthorizationCode_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class ExampleOAuth2Api implements ICredentialType {
	name = 'exampleOAuth2Api';

	extends = ['oAuth2Api'];

	displayName = 'Example OAuth2 API';

	// Link to your community node's README
	documentationUrl = 'https://github.com/org/repo?tab=readme-ov-file#credentials';

	properties: INodeProperties[] = [
		{
			displayName: 'Grant Type',
			name: 'grantType',
			type: 'hidden',
			default: 'authorizationCode',
		},
		{
			displayName: 'Authorization URL',
			name: 'authUrl',
			type: 'hidden',
			default: 'https://api.example.com/oauth/authorize',
		},
		{
			displayName: 'Access Token URL',
			name: 'accessTokenUrl',
			type: 'hidden',
			default: 'https://api.example.com/oauth/token',
		},
		{
			displayName: 'Auth URI Query Parameters',
			name: 'authQueryParameters',
			type: 'hidden',
			default: '',
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default: 'users:read users:write companies:read',
		},
		{
			displayName: 'Authentication',
			name: 'authentication',
			type: 'hidden',
			default: 'header',
		},
	];
}
