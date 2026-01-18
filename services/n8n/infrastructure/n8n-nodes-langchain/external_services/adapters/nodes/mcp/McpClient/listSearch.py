"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/mcp/McpClient/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/mcp/McpClient 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../shared/types。导出:无。关键函数/方法:getTools。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/mcp/McpClient/listSearch.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/mcp/McpClient/listSearch.py

import type { ILoadOptionsFunctions, INodeListSearchResult } from 'n8n-workflow';

import type { McpAuthenticationOption, McpServerTransport } from '../shared/types';
import {
	connectMcpClient,
	getAuthHeaders,
	mapToNodeOperationError,
	tryRefreshOAuth2Token,
} from '../shared/utils';

export async function getTools(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const authentication = this.getNodeParameter('authentication') as McpAuthenticationOption;
	const serverTransport = this.getNodeParameter('serverTransport') as McpServerTransport;
	const endpointUrl = this.getNodeParameter('endpointUrl') as string;
	const node = this.getNode();
	const { headers } = await getAuthHeaders(this, authentication);
	const client = await connectMcpClient({
		serverTransport,
		endpointUrl,
		headers,
		name: node.type,
		version: node.typeVersion,
		onUnauthorized: async (headers) => await tryRefreshOAuth2Token(this, authentication, headers),
	});

	if (!client.ok) {
		throw mapToNodeOperationError(node, client.error);
	}

	const result = await client.result.listTools({ cursor: paginationToken });
	const tools = filter
		? result.tools.filter((tool) => tool.name.toLowerCase().includes(filter.toLowerCase()))
		: result.tools;

	return {
		results: tools.map((tool) => ({
			name: tool.name,
			value: tool.name,
			description: tool.description,
			inputSchema: tool.inputSchema,
		})),
		paginationToken: result.nextCursor,
	};
}
