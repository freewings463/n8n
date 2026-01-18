"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/WhatsAppTriggerApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:WhatsAppTriggerApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/WhatsAppTriggerApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/WhatsAppTriggerApi_credentials.py

import type { ICredentialTestRequest, ICredentialType, INodeProperties } from 'n8n-workflow';

export class WhatsAppTriggerApi implements ICredentialType {
	name = 'whatsAppTriggerApi';

	displayName = 'WhatsApp OAuth API';

	documentationUrl = 'whatsapp';

	properties: INodeProperties[] = [
		{
			displayName: 'Client ID',
			name: 'clientId',
			type: 'string',
			default: '',
			required: true,
		},
		{
			displayName: 'Client Secret',
			name: 'clientSecret',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
			required: true,
		},
	];

	test: ICredentialTestRequest = {
		request: {
			method: 'POST',
			baseURL: 'https://graph.facebook.com/v19.0/oauth/access_token',
			body: {
				client_id: '={{$credentials.clientId}}',
				client_secret: '={{$credentials.clientSecret}}',
				grant_type: 'client_credentials',
			},
		},
	};
}
