"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/mcp.constants.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/mcp 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:USER_CONNECTED_TO_MCP_EVENT、USER_CALLED_MCP_TOOL_EVENT、UNAUTHORIZED_ERROR_MESSAGE、INTERNAL_SERVER_ERROR_MESSAGE、MCP_ACCESS_DISABLED_ERROR_MESSAGE、SUPPORTED_MCP_TRIGGERS。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/mcp.constants.ts -> services/n8n/application/cli/services/modules/mcp/mcp_constants.py

import {
	CHAT_TRIGGER_NODE_TYPE,
	FORM_TRIGGER_NODE_TYPE,
	SCHEDULE_TRIGGER_NODE_TYPE,
	WEBHOOK_NODE_TYPE,
} from 'n8n-workflow';

export const USER_CONNECTED_TO_MCP_EVENT = 'User connected to MCP server';
export const USER_CALLED_MCP_TOOL_EVENT = 'User called mcp tool';

export const UNAUTHORIZED_ERROR_MESSAGE = 'Unauthorized';
export const INTERNAL_SERVER_ERROR_MESSAGE = 'Internal server error';
export const MCP_ACCESS_DISABLED_ERROR_MESSAGE = 'MCP access is disabled';

export const SUPPORTED_MCP_TRIGGERS = {
	[SCHEDULE_TRIGGER_NODE_TYPE]: 'Schedule Trigger',
	[WEBHOOK_NODE_TYPE]: 'Webhook Trigger',
	[FORM_TRIGGER_NODE_TYPE]: 'Form Trigger',
	[CHAT_TRIGGER_NODE_TYPE]: 'Chat Trigger',
};
