"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/YouTubeOAuth2Api.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的OAuth凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:YouTubeOAuth2Api。关键函数/方法:无。用于声明 n8n OAuth鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/YouTubeOAuth2Api.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/YouTubeOAuth2Api_credentials.py

import type { ICredentialType, INodeProperties, Icon } from 'n8n-workflow';

//https://developers.google.com/youtube/v3/guides/auth/client-side-web-apps#identify-access-scopes
const scopes = [
	'https://www.googleapis.com/auth/youtube',
	'https://www.googleapis.com/auth/youtubepartner',
	'https://www.googleapis.com/auth/youtube.force-ssl',
	'https://www.googleapis.com/auth/youtube.upload',
	'https://www.googleapis.com/auth/youtubepartner-channel-audit',
];

export class YouTubeOAuth2Api implements ICredentialType {
	name = 'youTubeOAuth2Api';

	icon: Icon = 'node:n8n-nodes-base.youTube';

	extends = ['googleOAuth2Api'];

	displayName = 'YouTube OAuth2 API';

	documentationUrl = 'google';

	properties: INodeProperties[] = [
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default: scopes.join(' '),
		},
	];
}
