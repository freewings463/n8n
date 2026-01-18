"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MailerLiteApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:MailerLiteApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MailerLiteApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MailerLiteApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class MailerLiteApi implements ICredentialType {
	name = 'mailerLiteApi';

	displayName = 'Mailer Lite API';

	documentationUrl = 'mailerlite';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'Classic API',
			name: 'classicApi',
			type: 'boolean',
			default: true,
			description:
				'If the Classic API should be used, If this is your first time using this node this should be false.',
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		if (credentials.classicApi === true) {
			requestOptions.headers = {
				'X-MailerLite-ApiKey': credentials.apiKey as string,
			};
		} else {
			requestOptions.headers = {
				Authorization: `Bearer ${credentials.apiKey as string}`,
			};
		}
		return requestOptions;
	}

	test: ICredentialTestRequest = {
		request: {
			baseURL:
				'={{$credentials.classicApi ? "https://api.mailerlite.com/api/v2" : "https://connect.mailerlite.com/api"}}',
			url: '/groups',
		},
	};
}
