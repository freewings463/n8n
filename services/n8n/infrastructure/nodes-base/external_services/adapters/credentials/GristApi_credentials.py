"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/GristApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:GristApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/GristApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/GristApi_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class GristApi implements ICredentialType {
	name = 'gristApi';

	displayName = 'Grist API';

	documentationUrl = 'grist';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: true,
		},
		{
			displayName: 'Plan Type',
			name: 'planType',
			type: 'options',
			default: 'free',
			options: [
				{
					name: 'Free',
					value: 'free',
				},
				{
					name: 'Paid',
					value: 'paid',
				},
				{
					name: 'Self-Hosted',
					value: 'selfHosted',
				},
			],
		},
		{
			displayName: 'Custom Subdomain',
			name: 'customSubdomain',
			type: 'string',
			default: '',
			required: true,
			description: 'Custom subdomain of your team',
			displayOptions: {
				show: {
					planType: ['paid'],
				},
			},
		},
		{
			displayName: 'Self-Hosted URL',
			name: 'selfHostedUrl',
			type: 'string',
			default: '',
			placeholder: 'http://localhost:8484',
			required: true,
			description:
				'URL of your Grist instance. Include http/https without /api and no trailing slash.',
			displayOptions: {
				show: {
					planType: ['selfHosted'],
				},
			},
		},
	];
}
