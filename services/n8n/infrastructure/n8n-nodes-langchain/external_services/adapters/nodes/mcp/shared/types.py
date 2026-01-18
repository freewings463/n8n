"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/mcp/shared/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/mcp/shared 的类型。导入/依赖:外部:json-schema；内部:无；本地:无。导出:McpTool、McpServerTransport、McpAuthenticationOption。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/mcp/shared/types.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/mcp/shared/types.py

import type { JSONSchema7 } from 'json-schema';

export type McpTool = { name: string; description?: string; inputSchema: JSONSchema7 };

export type McpServerTransport = 'sse' | 'httpStreamable';

export type McpAuthenticationOption =
	| 'none'
	| 'headerAuth'
	| 'bearerAuth'
	| 'mcpOAuth2Api'
	| 'multipleHeadersAuth';
