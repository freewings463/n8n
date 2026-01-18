"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/HaloPSAApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:HaloPSAApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/HaloPSAApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/HaloPSAApi_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class HaloPSAApi implements ICredentialType {
	name = 'haloPSAApi';

	displayName = 'HaloPSA API';

	documentationUrl = 'halopsa';

	properties: INodeProperties[] = [
		{
			displayName: 'Hosting Type',
			name: 'hostingType',
			type: 'options',
			options: [
				{
					name: 'On-Premise Solution',
					value: 'onPremise',
				},
				{
					name: 'Hosted Solution Of Halo',
					value: 'hostedHalo',
				},
			],
			default: 'onPremise',
		},
		{
			displayName: 'HaloPSA Authorisation Server URL',
			name: 'authUrl',
			type: 'string',
			default: '',
			required: true,
		},
		{
			displayName: 'Resource Server',
			name: 'resourceApiUrl',
			type: 'string',
			default: '',
			required: true,
			description: 'The Resource server is available at your "Halo Web Application URL/api"',
		},
		{
			displayName: 'Client ID',
			name: 'client_id',
			type: 'string',
			default: '',
			required: true,
			description: 'Must be your application client ID',
		},
		{
			displayName: 'Client Secret',
			name: 'client_secret',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: true,
			description: 'Must be your application client secret',
		},
		{
			displayName: 'Tenant',
			name: 'tenant',
			type: 'string',
			displayOptions: {
				show: {
					hostingType: ['hostedHalo'],
				},
			},
			default: '',
			description: 'An additional tenant parameter for HaloPSA hosted solution',
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default: 'admin edit:tickets edit:customers',
			required: true,
		},
	];
}
