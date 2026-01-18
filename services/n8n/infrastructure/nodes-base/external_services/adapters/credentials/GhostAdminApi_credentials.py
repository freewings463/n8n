"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/GhostAdminApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:jsonwebtoken；内部:无；本地:无。导出:GhostAdminApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/GhostAdminApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/GhostAdminApi_credentials.py

import jwt from 'jsonwebtoken';
import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class GhostAdminApi implements ICredentialType {
	name = 'ghostAdminApi';

	displayName = 'Ghost Admin API';

	documentationUrl = 'ghost';

	properties: INodeProperties[] = [
		{
			displayName: 'URL',
			name: 'url',
			type: 'string',
			default: '',
			placeholder: 'http://localhost:3001',
		},
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
		const [id, secret] = (credentials.apiKey as string).split(':');
		const token = jwt.sign({}, Buffer.from(secret, 'hex'), {
			keyid: id,
			algorithm: 'HS256',
			expiresIn: '5m',
			audience: '/v2/admin/',
		});

		requestOptions.headers = {
			...requestOptions.headers,
			Authorization: `Ghost ${token}`,
		};
		return requestOptions;
	}

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.url}}',
			url: '/ghost/api/v2/admin/pages/',
		},
	};
}
