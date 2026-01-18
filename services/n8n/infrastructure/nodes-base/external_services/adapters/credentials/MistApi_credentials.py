"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MistApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:MistApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MistApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MistApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
	Icon,
} from 'n8n-workflow';

export class MistApi implements ICredentialType {
	name = 'mistApi';

	displayName = 'Mist API';

	icon: Icon = 'file:icons/Mist.svg';

	documentationUrl = 'mist';

	httpRequestNode = {
		name: 'Mist',
		docsUrl: 'https://www.mist.com/documentation/mist-api-introduction/',
		apiBaseUrl: '',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'API Token',
			name: 'token',
			type: 'string',
			typeOptions: { password: true },
			required: true,
			default: '',
		},
		{
			displayName: 'Region',
			name: 'region',
			type: 'options',
			options: [
				{
					name: 'Europe',
					value: 'eu',
				},
				{
					name: 'Global',
					value: 'global',
				},
			],
			default: 'eu',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Token {{$credentials.token}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '=https://api{{$credentials.region === "eu" ? ".eu" : ""}}.mist.com',
			url: '/api/v1/self',
			method: 'GET',
		},
	};
}
