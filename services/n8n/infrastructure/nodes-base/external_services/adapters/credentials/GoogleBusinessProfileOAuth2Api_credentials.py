"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/GoogleBusinessProfileOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:GoogleBusinessProfileOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/GoogleBusinessProfileOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/GoogleBusinessProfileOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

const scopes = ['https://www.googleapis.com/auth/business.manage'];

export class GoogleBusinessProfileOAuth2Api implements ICredentialType {
	name = 'googleBusinessProfileOAuth2Api';

	extends = ['googleOAuth2Api'];

	displayName = 'Google Business Profile OAuth2 API';

	documentationUrl = 'google/oauth-single-service';

	properties: INodeProperties[] = [
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default: scopes.join(' '),
		},
		{
			displayName:
				'Make sure that you have fulfilled the prerequisites and requested access to Google Business Profile API. <a href="https://developers.google.com/my-business/content/prereqs" target="_blank">More info</a>. Also, make sure that you have enabled the following APIs & Services in the Google Cloud Console: Google My Business API, Google My Business Management API. <a href="https://docs.n8n.io/integrations/builtin/credentials/google/oauth-generic/#scopes" target="_blank">More info</a>.',
			name: 'notice',
			type: 'notice',
			default: '',
		},
	];
}
