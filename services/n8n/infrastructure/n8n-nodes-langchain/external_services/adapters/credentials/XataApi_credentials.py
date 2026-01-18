"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/credentials/XataApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:XataApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/credentials/XataApi.credentials.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/credentials/XataApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class XataApi implements ICredentialType {
	name = 'xataApi';

	displayName = 'Xata Api';

	documentationUrl = 'xata';

	properties: INodeProperties[] = [
		{
			displayName: 'Database Endpoint',
			name: 'databaseEndpoint',
			required: true,
			type: 'string',
			default: '',
			placeholder: 'https://{workspace}.{region}.xata.sh/db/{database}',
		},
		{
			displayName: 'Branch',
			name: 'branch',
			required: true,
			type: 'string',
			default: 'main',
		},
		{
			displayName: 'API Key',
			name: 'apiKey',
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
				Authorization: '=Bearer {{$credentials.apiKey}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.databaseEndpoint}}:{{$credentials.branch}}',
		},
	};
}
