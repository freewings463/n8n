"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/mcp.utils.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/mcp 的模块。导入/依赖:外部:express；内部:@n8n/db、n8n-workflow；本地:./mcp.constants、./mcp.typeguards。导出:getClientInfo、getToolName、getToolArguments、findMcpSupportedTrigger。关键函数/方法:getClientInfo、getToolName、getToolArguments、findMcpSupportedTrigger。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/mcp.utils.ts -> services/n8n/presentation/cli/api/modules/mcp/mcp_utils.py

import type { AuthenticatedRequest } from '@n8n/db';
import type { Request } from 'express';
import type { INode } from 'n8n-workflow';

import { SUPPORTED_MCP_TRIGGERS } from './mcp.constants';
import { isRecord, isJSONRPCRequest } from './mcp.typeguards';

export const getClientInfo = (req: Request | AuthenticatedRequest) => {
	let clientInfo: { name?: string; version?: string } | undefined;
	if (isJSONRPCRequest(req.body) && req.body.params?.clientInfo) {
		clientInfo = req.body.params.clientInfo;
	}
	return clientInfo;
};

/**
 * Safely extracts the tool name from a JSON-RPC request
 * @param body - The request body to extract tool name from
 * @returns The tool name if valid, 'unknown' otherwise
 */
export const getToolName = (body: unknown): string => {
	if (!isJSONRPCRequest(body)) return 'unknown';
	if (!body.params) return 'unknown';

	const { name } = body.params;
	if (typeof name === 'string') {
		return name;
	}

	return 'unknown';
};

/**
 * Safely extracts tool arguments from a JSON-RPC request
 * @param body - The request body to extract arguments from
 * @returns The arguments object if valid, empty object otherwise
 */
export const getToolArguments = (body: unknown): Record<string, unknown> => {
	if (!isJSONRPCRequest(body)) return {};
	if (!body.params) return {};

	const { arguments: args } = body.params;
	if (isRecord(args)) {
		return args;
	}

	return {};
};

/**
 * Finds the first supported trigger node in the provided nodes array.
 * Workflow is eligible for MCP access if it contains at least one of these (enabled) trigger nodes:
 * - Schedule trigger
 * - Webhook trigger
 * - Form trigger
 * - Chat trigger
 */
export const findMcpSupportedTrigger = (nodes: INode[]): INode | undefined => {
	const triggerNodeTypes = Object.keys(SUPPORTED_MCP_TRIGGERS);
	return nodes.find((node) => triggerNodeTypes.includes(node.type) && !node.disabled);
};
