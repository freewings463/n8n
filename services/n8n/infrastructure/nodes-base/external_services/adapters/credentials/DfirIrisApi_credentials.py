"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/DfirIrisApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:DfirIrisApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/DfirIrisApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/DfirIrisApi_credentials.py

import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class DfirIrisApi implements ICredentialType {
	name = 'dfirIrisApi';

	displayName = 'DFIR-IRIS API';

	documentationUrl = 'dfiriris';

	icon = { light: 'file:icons/DfirIris.svg', dark: 'file:icons/DfirIris.svg' } as const;

	httpRequestNode = {
		name: 'DFIR-IRIS',
		docsUrl: 'https://docs.dfir-iris.org/operations/api/',
		apiBaseUrlPlaceholder: 'http://<yourserver_ip>/manage/cases/list',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'Base URL',
			name: 'baseUrl',
			type: 'string',
			default: '',
			placeholder: 'e.g. https://localhost',
			description:
				'The API endpoints are reachable on the same Address and port as the web interface.',
			required: true,
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
			displayName: 'Ignore SSL Issues (Insecure)',
			name: 'skipSslCertificateValidation',
			type: 'boolean',
			default: false,
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials.apiKey}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.baseUrl}}',
			url: '/api/ping',
			method: 'GET',
			skipSslCertificateValidation: '={{$credentials.skipSslCertificateValidation}}',
		},
	};
}
