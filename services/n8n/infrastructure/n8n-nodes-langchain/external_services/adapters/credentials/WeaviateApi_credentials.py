"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/credentials/WeaviateApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:WeaviateApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/credentials/WeaviateApi.credentials.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/credentials/WeaviateApi_credentials.py

import type { ICredentialTestRequest, ICredentialType, INodeProperties } from 'n8n-workflow';

export class WeaviateApi implements ICredentialType {
	name = 'weaviateApi';

	displayName = 'Weaviate Credentials';

	documentationUrl = 'https://docs.n8n.io/integrations/builtin/credentials/weaviate/';

	properties: INodeProperties[] = [
		{
			displayName: 'Connection Type',
			name: 'connection_type',
			type: 'options',
			options: [
				{
					name: 'Weaviate Cloud',
					value: 'weaviate_cloud',
				},
				{
					name: 'Custom Connection',
					value: 'custom_connection',
				},
			],
			default: 'weaviate_cloud',
			description:
				'Choose whether to connect to a Weaviate Cloud instance or a custom Weaviate instance.',
		},
		{
			displayName: 'Weaviate Cloud Endpoint',
			name: 'weaviate_cloud_endpoint',
			description: 'The Endpoint of a Weaviate Cloud instance.',
			placeholder: 'https://your-cluster.weaviate.cloud',
			type: 'string',
			required: true,
			default: '',
			displayOptions: {
				show: {
					connection_type: ['weaviate_cloud'],
				},
			},
		},
		{
			displayName: 'Weaviate Api Key',
			name: 'weaviate_api_key',
			description: 'The API key for the Weaviate instance.',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'Custom Connection HTTP Host',
			name: 'custom_connection_http_host',
			description: 'The host of your Weaviate instance.',
			type: 'string',
			required: true,
			default: 'weaviate',
			displayOptions: {
				show: {
					connection_type: ['custom_connection'],
				},
			},
		},
		{
			displayName: 'Custom Connection HTTP Port',
			name: 'custom_connection_http_port',
			description: 'The port of your Weaviate instance.',
			type: 'number',
			required: true,
			default: 8080,
			displayOptions: {
				show: {
					connection_type: ['custom_connection'],
				},
			},
		},
		{
			displayName: 'Custom Connection HTTP Secure',
			name: 'custom_connection_http_secure',
			description: 'Whether to use a secure connection for HTTP.',
			type: 'boolean',
			required: true,
			default: false,
			displayOptions: {
				show: {
					connection_type: ['custom_connection'],
				},
			},
		},
		{
			displayName: 'Custom Connection gRPC Host',
			name: 'custom_connection_grpc_host',
			description: 'The gRPC host of your Weaviate instance.',
			type: 'string',
			required: true,
			default: 'weaviate',
			displayOptions: {
				show: {
					connection_type: ['custom_connection'],
				},
			},
		},
		{
			displayName: 'Custom Connection gRPC Port',
			name: 'custom_connection_grpc_port',
			description: 'The gRPC port of your Weaviate instance.',
			type: 'number',
			required: true,
			default: 50051,
			displayOptions: {
				show: {
					connection_type: ['custom_connection'],
				},
			},
		},
		{
			displayName: 'Custom Connection gRPC Secure',
			name: 'custom_connection_grpc_secure',
			description: 'Whether to use a secure connection for gRPC.',
			type: 'boolean',
			required: true,
			default: false,
			displayOptions: {
				show: {
					connection_type: ['custom_connection'],
				},
			},
		},
	];

	test: ICredentialTestRequest = {
		request: {
			baseURL:
				'={{$credentials.weaviate_cloud_endpoint?$credentials.weaviate_cloud_endpoint.startsWith("http://") || $credentials.weaviate_cloud_endpoint.startsWith("https://")?$credentials.weaviate_cloud_endpoint:"https://" + $credentials.weaviate_cloud_endpoint:($credentials.custom_connection_http_secure ? "https" : "http") + "://" + $credentials.custom_connection_http_host + ":" + $credentials.custom_connection_http_port }}',
			url: '/v1/nodes',
			disableFollowRedirect: false,
			headers: {
				Authorization:
					'={{$if($credentials.weaviate_api_key, "Bearer " + $credentials.weaviate_api_key, undefined)}}',
			},
		},
	};
}
