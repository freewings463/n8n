"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:RequestResponseMetadata、IntermediateStep、AgentOptions。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/types.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/ToolsAgent/V3/types.py

import type {
	ToolCallData,
	ToolCallRequest,
	AgentResult,
	RequestResponseMetadata as SharedRequestResponseMetadata,
} from '@utils/agent-execution';

// Re-export shared types for backwards compatibility
export type { ToolCallData, ToolCallRequest, AgentResult };

// Use the shared metadata type directly (it already includes previousRequests)
export type RequestResponseMetadata = SharedRequestResponseMetadata;

// Keep the IntermediateStep type for compatibility
export type IntermediateStep = {
	action: {
		tool: string;
		toolInput: Record<string, unknown>;
		log: string;
		messageLog: unknown[];
		toolCallId: string;
		type: string;
	};
	observation?: string;
};

export type AgentOptions = {
	systemMessage?: string;
	maxIterations?: number;
	returnIntermediateSteps?: boolean;
	passthroughBinaryImages?: boolean;
	enableStreaming?: boolean;
	maxTokensFromMemory?: number;
};
