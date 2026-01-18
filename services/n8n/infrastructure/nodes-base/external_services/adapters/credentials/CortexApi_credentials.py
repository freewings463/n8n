"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/CortexApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:CortexApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/CortexApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/CortexApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class CortexApi implements ICredentialType {
	name = 'cortexApi';

	displayName = 'Cortex API';

	documentationUrl = 'cortex';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'cortexApiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'Cortex Instance',
			name: 'host',
			type: 'string',
			description: 'The URL of the Cortex instance',
			default: '',
			placeholder: 'https://localhost:9001',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials.cortexApiKey}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.host}}',
			url: '/api/analyzer',
		},
	};
}
