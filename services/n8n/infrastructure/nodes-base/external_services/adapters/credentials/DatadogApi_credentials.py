"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/DatadogApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:DatadogApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/DatadogApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/DatadogApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class DatadogApi implements ICredentialType {
	name = 'datadogApi';

	displayName = 'Datadog API';

	documentationUrl = 'datadog';

	icon = { light: 'file:icons/Datadog.svg', dark: 'file:icons/Datadog.svg' } as const;

	httpRequestNode = {
		name: 'Datadog',
		docsUrl: 'https://docs.datadoghq.com/api/latest/',
		apiBaseUrlPlaceholder: 'https://api.datadoghq.com/api/v1/metrics',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'URL',
			name: 'url',
			required: true,
			type: 'string',
			default: 'https://api.datadoghq.com',
		},
		{
			displayName: 'API Key',
			name: 'apiKey',
			required: true,
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'APP Key',
			name: 'appKey',
			required: false,
			type: 'string',
			default: '',
			typeOptions: { password: true },
			description: 'For some endpoints, you also need an Application key.',
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		requestOptions.headers = {
			'DD-API-KEY': credentials.apiKey,
			'DD-APPLICATION-KEY': credentials.appKey,
		};
		if (!requestOptions.headers['DD-APPLICATION-KEY']) {
			delete requestOptions.headers['DD-APPLICATION-KEY'];
		}

		return requestOptions;
	}

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.url}}',
			url: '/api/v1/validate',
			method: 'GET',
		},
	};
}
