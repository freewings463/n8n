"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/StripeApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:StripeApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/StripeApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/StripeApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class StripeApi implements ICredentialType {
	name = 'stripeApi';

	displayName = 'Stripe API';

	documentationUrl = 'stripe';

	properties: INodeProperties[] = [
		{
			displayName: 'Secret Key',
			name: 'secretKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'Signature Secret',
			name: 'signatureSecret',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			description:
				'The signature secret is used to verify the authenticity of requests sent by Stripe.',
		},
		{
			displayName:
				'We strongly recommend setting up a <a href="https://stripe.com/docs/webhooks" target="_blank">signing secret</a> to ensure the authenticity of requests.',
			name: 'notice',
			type: 'notice',
			default: '',
			displayOptions: {
				show: {
					signatureSecret: [''],
				},
			},
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials.secretKey}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: 'https://api.stripe.com/v1',
			url: '/charges',
			json: true,
		},
	};
}
