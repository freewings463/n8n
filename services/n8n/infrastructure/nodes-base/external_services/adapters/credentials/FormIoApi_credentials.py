"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/FormIoApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:FormIoApi。关键函数/方法:preAuthentication。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/FormIoApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/FormIoApi_credentials.py

import type {
	IAuthenticate,
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestHelper,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class FormIoApi implements ICredentialType {
	name = 'formIoApi';

	displayName = 'Form.io API';

	documentationUrl = 'formiotrigger';

	properties: INodeProperties[] = [
		{
			displayName: 'Environment',
			name: 'environment',
			type: 'options',
			default: 'cloudHosted',
			options: [
				{
					name: 'Cloud-Hosted',
					value: 'cloudHosted',
				},
				{
					name: 'Self-Hosted',
					value: 'selfHosted',
				},
			],
		},
		{
			displayName: 'Self-Hosted Domain',
			name: 'domain',
			type: 'string',
			default: '',
			placeholder: 'https://www.mydomain.com',
			displayOptions: {
				show: {
					environment: ['selfHosted'],
				},
			},
		},
		{
			displayName: 'Email',
			name: 'email',
			type: 'string',
			placeholder: 'name@email.com',
			default: '',
		},
		{
			displayName: 'Password',
			name: 'password',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
		},
		{
			displayName: 'Token',
			name: 'token',
			type: 'hidden',
			typeOptions: {
				expirable: true,
				password: true,
			},
			default: '',
		},
	];

	async preAuthentication(this: IHttpRequestHelper, credentials: ICredentialDataDecryptedObject) {
		const base = credentials.domain || 'https://formio.form.io';
		const options = {
			headers: {
				'Content-Type': 'application/json',
			},
			method: 'POST',
			body: {
				data: {
					email: credentials.email,
					password: credentials.password,
				},
			},
			url: `${base}/user/login`,
			json: true,
			returnFullResponse: true,
		} satisfies IHttpRequestOptions;

		const responseObject = await this.helpers.httpRequest(options);
		const token = responseObject.headers['x-jwt-token'];

		return { token };
	}

	authenticate: IAuthenticate = {
		type: 'generic',
		properties: {
			headers: {
				'x-jwt-token': '={{ $credentials.token }}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.domain || "https://formio.form.io"}}',
			url: 'current',
		},
	};
}
