"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/VenafiTlsProtectDatacenterApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:VenafiTlsProtectDatacenterApi。关键函数/方法:preAuthentication。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/VenafiTlsProtectDatacenterApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/VenafiTlsProtectDatacenterApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialDataDecryptedObject,
	ICredentialType,
	IHttpRequestHelper,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';

export class VenafiTlsProtectDatacenterApi implements ICredentialType {
	name = 'venafiTlsProtectDatacenterApi';

	displayName = 'Venafi TLS Protect Datacenter API';

	documentationUrl = 'venafitlsprotectdatacenter';

	properties: INodeProperties[] = [
		{
			displayName: 'Domain',
			name: 'domain',
			type: 'string',
			default: '',
			placeholder: 'https://example.com',
		},
		{
			displayName: 'Client ID',
			name: 'clientId',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Username',
			name: 'username',
			type: 'string',
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
			displayName: 'Allow Self-Signed Certificates',
			name: 'allowUnauthorizedCerts',
			type: 'boolean',
			default: true,
		},
		{
			displayName: 'Access Token',
			name: 'token',
			type: 'hidden',

			typeOptions: {
				expirable: true,
			},
			default: '',
		},
		{
			displayName: 'Scope',
			name: 'scope',
			type: 'hidden',
			default: 'certificate:manage',
		},
	];

	async preAuthentication(this: IHttpRequestHelper, credentials: ICredentialDataDecryptedObject) {
		const url = `${credentials.domain}/vedauth/authorize/oauth`;

		const requestOptions: IHttpRequestOptions = {
			url,
			method: 'POST',
			json: true,
			skipSslCertificateValidation: credentials.allowUnauthorizedCerts as boolean,
			body: {
				client_id: credentials.clientId,
				username: credentials.username,
				password: credentials.password,
				scope: credentials.scope,
			},
		};

		const { access_token } = (await this.helpers.httpRequest(requestOptions)) as {
			access_token: string;
		};

		return { token: access_token };
	}

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials.token}}',
			},
		},
	};
}
