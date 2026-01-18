"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/parent-graph-state.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src 的工作流模块。导入/依赖:外部:@langchain/core/messages、@langchain/langgraph；内部:无；本地:./types/coordination、./types/discovery-types、./types/tools、./types/workflow 等2项。导出:ParentGraphState。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/parent-graph-state.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/parent_graph_state.py

import type { BaseMessage } from '@langchain/core/messages';
import { Annotation, messagesStateReducer } from '@langchain/langgraph';

import type { CoordinationLogEntry } from './types/coordination';
import type { DiscoveryContext } from './types/discovery-types';
import type { WorkflowMetadata } from './types/tools';
import type { SimpleWorkflow, WorkflowOperation } from './types/workflow';
import { appendArrayReducer, cachedTemplatesReducer } from './utils/state-reducers';
import type { ChatPayload } from './workflow-builder-agent';

/**
 * Parent Graph State
 *
 * Minimal state that coordinates between subgraphs.
 * Each subgraph has its own isolated state.
 */
export const ParentGraphState = Annotation.Root({
	// Shared: User's conversation history (for responder)
	messages: Annotation<BaseMessage[]>({
		reducer: messagesStateReducer,
		default: () => [],
	}),

	// Shared: Current workflow being built
	workflowJSON: Annotation<SimpleWorkflow>({
		reducer: (x, y) => y ?? x,
		default: () => ({ nodes: [], connections: {}, name: '' }),
	}),

	// Input: Workflow context (execution data)
	workflowContext: Annotation<ChatPayload['workflowContext'] | undefined>({
		reducer: (x, y) => y ?? x,
	}),

	// Routing: Next phase to execute
	nextPhase: Annotation<string>({
		reducer: (x, y) => y ?? x,
		default: () => '',
	}),

	// Discovery context to pass to other agents
	discoveryContext: Annotation<DiscoveryContext | null>({
		reducer: (x, y) => y ?? x,
		default: () => null,
	}),

	// Workflow operations collected from subgraphs (hybrid approach)
	workflowOperations: Annotation<WorkflowOperation[]>({
		reducer: (x, y) => x.concat(y),
		default: () => [],
	}),

	// Coordination log for tracking subgraph completion (deterministic routing)
	coordinationLog: Annotation<CoordinationLogEntry[]>({
		reducer: (x, y) => x.concat(y),
		default: () => [],
	}),

	// For conversation compaction - stores summarized history
	previousSummary: Annotation<string>({
		reducer: (x, y) => y ?? x,
		default: () => '',
	}),

	// Template IDs fetched from workflow examples for telemetry
	templateIds: Annotation<number[]>({
		reducer: appendArrayReducer,
		default: () => [],
	}),

	// Cached workflow templates from template API
	// Shared across subgraphs to reduce API calls
	cachedTemplates: Annotation<WorkflowMetadata[]>({
		reducer: cachedTemplatesReducer,
		default: () => [],
	}),
});
