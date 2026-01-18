"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/mcp/shared/descriptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/mcp/shared 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:transportSelect、credentials。关键函数/方法:transportSelect。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/mcp/shared/descriptions.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/mcp/shared/descriptions.py

import type { IDisplayOptions, INodeCredentialDescription, INodeProperties } from 'n8n-workflow';

export const transportSelect = ({
	defaultOption,
	displayOptions,
}: {
	defaultOption: 'sse' | 'httpStreamable';
	displayOptions?: IDisplayOptions;
}): INodeProperties => ({
	displayName: 'Server Transport',
	name: 'serverTransport',
	type: 'options',
	options: [
		{
			name: 'HTTP Streamable',
			value: 'httpStreamable',
		},
		{
			name: 'Server Sent Events (Deprecated)',
			value: 'sse',
		},
	],
	default: defaultOption,
	description: 'The transport used by your endpoint',
	displayOptions,
});

export const credentials: INodeCredentialDescription[] = [
	{
		name: 'httpBearerAuth',
		required: true,
		displayOptions: {
			show: {
				authentication: ['bearerAuth'],
			},
		},
	},
	{
		name: 'httpHeaderAuth',
		required: true,
		displayOptions: {
			show: {
				authentication: ['headerAuth'],
			},
		},
	},
	{
		name: 'mcpOAuth2Api',
		required: true,
		displayOptions: {
			show: {
				authentication: ['mcpOAuth2Api'],
			},
		},
	},
	{
		name: 'httpMultipleHeadersAuth',
		required: true,
		displayOptions: {
			show: {
				authentication: ['multipleHeadersAuth'],
			},
		},
	},
];
