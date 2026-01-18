"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/MindeeReceiptApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:MindeeReceiptApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/MindeeReceiptApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/MindeeReceiptApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class MindeeReceiptApi implements ICredentialType {
	name = 'mindeeReceiptApi';

	displayName = 'Mindee Receipt API';

	documentationUrl = 'mindee';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		// @ts-ignore
		const url = new URL(requestOptions.url ? requestOptions.url : requestOptions.uri);
		if (url.hostname === 'api.mindee.net' && url.pathname.startsWith('/v1/')) {
			requestOptions.headers!.Authorization = `Token ${credentials.apiKey}`;
		} else {
			requestOptions.headers!['X-Inferuser-Token'] = `${credentials.apiKey}`;
		}
		return requestOptions;
	}
}
