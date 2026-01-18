"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/ActionNetworkApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:ActionNetworkApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/ActionNetworkApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/ActionNetworkApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class ActionNetworkApi implements ICredentialType {
	name = 'actionNetworkApi';

	displayName = 'Action Network API';

	documentationUrl = 'actionnetwork';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
	];

	test: ICredentialTestRequest = {
		request: {
			baseURL: 'https://actionnetwork.org/api/v2',
			url: '/events?per_page=1',
		},
	};

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		requestOptions.headers = { 'OSDI-API-Token': credentials.apiKey };
		return requestOptions;
	}
}
