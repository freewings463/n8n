"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/ElasticSecurityApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:ElasticSecurityApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/ElasticSecurityApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/ElasticSecurityApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class ElasticSecurityApi implements ICredentialType {
	name = 'elasticSecurityApi';

	displayName = 'Elastic Security API';

	documentationUrl = 'elasticsecurity';

	properties: INodeProperties[] = [
		{
			displayName: 'Base URL',
			name: 'baseUrl',
			type: 'string',
			default: '',
			placeholder: 'e.g. https://mydeployment.kb.us-central1.gcp.cloud.es.io:9243',
			description: "Referred to as Kibana 'endpoint' in the Elastic deployment dashboard",
			required: true,
		},
		{
			displayName: 'Type',
			name: 'type',
			type: 'options',
			options: [
				{
					name: 'API Key',
					value: 'apiKey',
				},
				{
					name: 'Basic Auth',
					value: 'basicAuth',
				},
			],
			default: 'basicAuth',
		},
		{
			displayName: 'Username',
			name: 'username',
			type: 'string',
			default: '',
			required: true,
			displayOptions: {
				show: {
					type: ['basicAuth'],
				},
			},
		},
		{
			displayName: 'Password',
			name: 'password',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
			required: true,
			displayOptions: {
				show: {
					type: ['basicAuth'],
				},
			},
		},
		{
			displayName: 'API Key',
			name: 'apiKey',
			required: true,
			type: 'string',
			typeOptions: { password: true },
			default: '',
			displayOptions: {
				show: {
					type: ['apiKey'],
				},
			},
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		if (credentials.type === 'apiKey') {
			requestOptions.headers = {
				Authorization: `ApiKey ${credentials.apiKey}`,
			};
		} else {
			requestOptions.auth = {
				username: credentials.username as string,
				password: credentials.password as string,
			};
			requestOptions.headers = {
				'kbn-xsrf': true,
			};
		}
		return requestOptions;
	}

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.baseUrl}}',
			url: '/api/endpoint/metadata',
			method: 'GET',
		},
	};
}
