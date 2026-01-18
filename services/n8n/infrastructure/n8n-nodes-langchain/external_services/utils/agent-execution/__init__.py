"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/agent-execution/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils/agent-execution 的执行入口。导入/依赖:外部:无；内部:无；本地:无。导出:createEngineRequests、buildSteps、processEventStream、loadMemory、saveToMemory、buildToolContext。关键函数/方法:无。用于汇总导出并完成执行模块初始化、注册或装配。注释目标:Agent Execution Utilities / This module contains generalized utilities for agent execution that can be。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/agent-execution/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/agent-execution/__init__.py

/**
 * Agent Execution Utilities
 *
 * This module contains generalized utilities for agent execution that can be
 * reused across different agent types (Tools Agent, OpenAI Functions Agent, etc.).
 *
 * These utilities support engine-based tool execution, where tool calls are
 * delegated to the n8n workflow engine instead of being executed inline.
 */

export { createEngineRequests } from './createEngineRequests';
export { buildSteps } from './buildSteps';
export { processEventStream } from './processEventStream';
export { loadMemory, saveToMemory, buildToolContext } from './memoryManagement';
export type {
	ToolCallRequest,
	ToolCallData,
	AgentResult,
	RequestResponseMetadata,
} from './types';
