"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/AirtableTokenApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:AirtableTokenApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/AirtableTokenApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/AirtableTokenApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class AirtableTokenApi implements ICredentialType {
	name = 'airtableTokenApi';

	displayName = 'Airtable Personal Access Token API';

	documentationUrl = 'airtable';

	properties: INodeProperties[] = [
		{
			displayName: 'Access Token',
			name: 'accessToken',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: `Make sure you enabled the following scopes for your token:<br>
				<code>data.records:read</code><br>
				<code>data.records:write</code><br>
				<code>schema.bases:read</code><br>
				`,
			name: 'notice',
			type: 'notice',
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
			baseURL: 'https://api.airtable.com/v0/meta/whoami',
		},
	};
}
