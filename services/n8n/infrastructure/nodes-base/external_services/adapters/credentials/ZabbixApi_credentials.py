"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/ZabbixApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:ZabbixApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/ZabbixApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/ZabbixApi_credentials.py

import type {
	IAuthenticateGeneric,
	Icon,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class ZabbixApi implements ICredentialType {
	name = 'zabbixApi';

	displayName = 'Zabbix API';

	documentationUrl = 'zabbix';

	icon: Icon = 'file:icons/Zabbix.svg';

	httpRequestNode = {
		name: 'Zabbix',
		docsUrl: 'https://www.zabbix.com/documentation/current/en/manual/api',
		apiBaseUrl: '',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'URL',
			name: 'url',
			required: true,
			type: 'string',
			default: '',
		},
		{
			displayName: 'API Token',
			name: 'apiToken',
			required: true,
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				Authorization: '=Bearer {{$credentials.apiToken}}',
				'Content-Type': 'application/json-rpc',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.url}}'.replace(/\/$/, ''),
			url: '/api_jsonrpc.php',
			method: 'POST',
			body: {
				jsonrpc: '2.0',
				method: 'host.get',
				params: {
					output: ['hostid', 'host'],
					selectInterfaces: ['interfaceid', 'ip'],
				},
				id: 2,
			},
		},
		rules: [
			{
				type: 'responseSuccessBody',
				properties: {
					key: 'result',
					value: undefined,
					message: 'Invalid access token',
				},
			},
		],
	};
}
