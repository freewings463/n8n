"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/mcp.types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/mcp 的类型。导入/依赖:外部:@modelcontextprotocol/sdk/…/mcp.js、zod；内部:@n8n/db、n8n-workflow；本地:./mcp.constants、./tools/get-workflow-details.tool。导出:ToolDefinition、SearchWorkflowsParams、SearchWorkflowsItem、SearchWorkflowsResult、WorkflowDetailsResult、WorkflowDetailsWorkflow、WorkflowDetailsNode、JSONRPCRequest 等8项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/mcp.types.ts -> services/n8n/application/cli/services/modules/mcp/mcp_types.py

import { type ToolCallback } from '@modelcontextprotocol/sdk/server/mcp.js';
import type { User } from '@n8n/db';
import type { INode } from 'n8n-workflow';
import type z from 'zod';

import type { SUPPORTED_MCP_TRIGGERS } from './mcp.constants';
import type { WorkflowDetailsOutputSchema } from './tools/get-workflow-details.tool';

export type ToolDefinition<InputArgs extends z.ZodRawShape = z.ZodRawShape> = {
	name: string;
	config: {
		description?: string;
		inputSchema?: InputArgs;
		outputSchema?: z.ZodRawShape;
		annotations?: {
			title?: string;
			readOnlyHint?: boolean;
			destructiveHint?: boolean;
			idempotentHint?: boolean;
			openWorldHint?: boolean;
		};
	};
	handler: ToolCallback<InputArgs>;
};

// Shared MCP tool types
export type SearchWorkflowsParams = {
	limit?: number;
	query?: string;
	projectId?: string;
};

export type SearchWorkflowsItem = {
	id: string;
	name: string | null;
	active: boolean | null;
	createdAt: string | null;
	updatedAt: string | null;
	triggerCount: number | null;
	nodes: Array<{ name: string; type: string }>;
};

export type SearchWorkflowsResult = {
	data: SearchWorkflowsItem[];
	count: number;
};

export type WorkflowDetailsResult = z.infer<WorkflowDetailsOutputSchema>;
export type WorkflowDetailsWorkflow = WorkflowDetailsResult['workflow'];
export type WorkflowDetailsNode = WorkflowDetailsWorkflow['nodes'][number];

// JSON-RPC types for MCP protocol
export type JSONRPCRequest = {
	jsonrpc?: string;
	method?: string;
	params?: {
		clientInfo?: {
			name?: string;
			version?: string;
		};
		[key: string]: unknown;
	};
	id?: string | number | null;
};

// Telemetry payloads
export type UserConnectedToMCPEventPayload = {
	user_id?: string;
	client_name?: string;
	client_version?: string;
	mcp_connection_status: 'success' | 'error';
	error?: string;
};

export type UserCalledMCPToolEventPayload = {
	user_id?: string;
	tool_name: string;
	parameters?: Record<string, unknown>;
	results?: {
		success: boolean;
		data?: unknown;
		error?: string;
	};
};

export type ExecuteWorkflowsInputMeta = {
	type: 'webhook' | 'chat' | 'schedule' | 'form';
	parameter_count: number;
};

type SupportedTriggerNodeTypes = keyof typeof SUPPORTED_MCP_TRIGGERS;

export type MCPTriggersMap = {
	[K in SupportedTriggerNodeTypes]: INode[];
};

export type AuthFailureReason =
	| 'missing_authorization_header'
	| 'invalid_bearer_format'
	| 'jwt_decode_failed'
	| 'invalid_token'
	| 'token_not_found_in_db'
	| 'user_not_found'
	| 'user_id_not_in_auth_info'
	| 'unknown_error';

export type Mcpauth_type = 'oauth' | 'api_key' | 'unknown';

export type TelemetryAuthContext = {
	reason: AuthFailureReason;
	auth_type: Mcpauth_type;
	error_details?: string;
};

export type UserWithContext = {
	user: User | null;
	context?: TelemetryAuthContext;
};
