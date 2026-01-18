"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/NextCloudApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:NextCloudApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/NextCloudApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/NextCloudApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class NextCloudApi implements ICredentialType {
	name = 'nextCloudApi';

	displayName = 'NextCloud API';

	documentationUrl = 'nextcloud';

	properties: INodeProperties[] = [
		{
			displayName: 'Web DAV URL',
			name: 'webDavUrl',
			type: 'string',
			placeholder: 'https://nextcloud.example.com/remote.php/webdav',
			default: '',
		},
		{
			displayName: 'User',
			name: 'user',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Password',
			name: 'password',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
	];

	async authenticate(
		credentials: ICredentialDataDecryptedObject,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		requestOptions.auth = {
			username: credentials.user as string,
			password: credentials.password as string,
		};
		return requestOptions;
	}

	test: ICredentialTestRequest = {
		request: {
			baseURL: "={{$credentials.webDavUrl.replace('/remote.php/webdav', '')}}",
			url: '/ocs/v1.php/cloud/capabilities',
			headers: { 'OCS-APIRequest': true },
		},
	};
}
