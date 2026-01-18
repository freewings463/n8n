"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/mcp/McpTrigger/FlushingTransport.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/mcp/McpTrigger 的节点。导入/依赖:外部:@modelcontextprotocol/sdk/…/sse.js、@modelcontextprotocol/sdk/…/streamableHttp.js、@modelcontextprotocol/sdk/types.js、express；内部:无；本地:无。导出:CompressionResponse、FlushingSSEServerTransport、FlushingStreamableHTTPTransport。关键函数/方法:send、handleRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/mcp/McpTrigger/FlushingTransport.ts -> services/n8n/presentation/n8n-nodes-langchain/api/nodes/mcp/McpTrigger/FlushingTransport.py

import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import type { StreamableHTTPServerTransportOptions } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import type { JSONRPCMessage } from '@modelcontextprotocol/sdk/types.js';
import type { Response } from 'express';
import type { IncomingMessage, ServerResponse } from 'http';

export type CompressionResponse = Response & {
	/**
	 * `flush()` is defined in the compression middleware.
	 * This is necessary because the compression middleware sometimes waits
	 * for a certain amount of data before sending the data to the client
	 */
	flush: () => void;
};

export class FlushingSSEServerTransport extends SSEServerTransport {
	constructor(
		_endpoint: string,
		private response: CompressionResponse,
	) {
		super(_endpoint, response);
	}

	async send(message: JSONRPCMessage): Promise<void> {
		await super.send(message);
		this.response.flush();
	}

	async handleRequest(
		req: IncomingMessage,
		resp: ServerResponse,
		message: IncomingMessage,
	): Promise<void> {
		await super.handlePostMessage(req, resp, message);
		this.response.flush();
	}
}

export class FlushingStreamableHTTPTransport extends StreamableHTTPServerTransport {
	private response: CompressionResponse;

	constructor(options: StreamableHTTPServerTransportOptions, response: CompressionResponse) {
		super(options);
		this.response = response;
	}

	async send(message: JSONRPCMessage): Promise<void> {
		await super.send(message);
		this.response.flush();
	}

	async handleRequest(
		req: IncomingMessage,
		resp: ServerResponse,
		parsedBody?: unknown,
	): Promise<void> {
		await super.handleRequest(req, resp, parsedBody);
		this.response.flush();
	}
}
