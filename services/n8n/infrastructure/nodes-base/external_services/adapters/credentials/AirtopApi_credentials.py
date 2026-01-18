"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/AirtopApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:../Airtop/constants。导出:AirtopApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/AirtopApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/AirtopApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialType,
	ICredentialTestRequest,
	INodeProperties,
} from 'n8n-workflow';

import { BASE_URL } from '../nodes/Airtop/constants';

export class AirtopApi implements ICredentialType {
	name = 'airtopApi';

	displayName = 'Airtop API';

	documentationUrl = 'airtop';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			default: '',
			description:
				'The Airtop API key. You can create one at <a href="https://portal.airtop.ai/api-keys" target="_blank">Airtop</a> for free.',
			required: true,
			typeOptions: {
				password: true,
			},
			noDataExpression: true,
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials.apiKey}}',
				'api-key': '={{$credentials.apiKey}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			method: 'GET',
			baseURL: BASE_URL,
			url: '/sessions',
			qs: {
				limit: 10,
			},
		},
	};
}
