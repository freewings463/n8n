"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/workflow-state.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src 的工作流模块。导入/依赖:外部:@langchain/core/messages、@langchain/langgraph；内部:无；本地:./types、./utils/state-reducers、./validation/types、./workflow-builder-agent。导出:createTrimMessagesReducer、WorkflowState。关键函数/方法:operationsReducer、createTrimMessagesReducer。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/workflow-state.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/workflow_state.py

import type { BaseMessage } from '@langchain/core/messages';
import { HumanMessage } from '@langchain/core/messages';
import { Annotation, messagesStateReducer } from '@langchain/langgraph';

import type { SimpleWorkflow, WorkflowMetadata, WorkflowOperation } from './types';
import { appendArrayReducer, cachedTemplatesReducer } from './utils/state-reducers';
import type { ProgrammaticEvaluationResult, TelemetryValidationStatus } from './validation/types';
import type { ChatPayload } from './workflow-builder-agent';

/**
 * Reducer for collecting workflow operations from parallel tool executions.
 * This reducer intelligently merges operations, avoiding duplicates and handling special cases.
 */
function operationsReducer(
	current: WorkflowOperation[] | null,
	update: WorkflowOperation[] | null | undefined,
): WorkflowOperation[] {
	if (update === null) {
		return [];
	}

	if (!update || update.length === 0) {
		return current ?? [];
	}

	// For clear operations, we can reset everything
	if (update.some((op) => op.type === 'clear')) {
		return update.filter((op) => op.type === 'clear').slice(-1); // Keep only the last clear
	}

	if (!current && !update) {
		return [];
	}
	// Otherwise, append new operations
	return [...(current ?? []), ...update];
}

// Creates a reducer that trims the message history to keep only the last `maxUserMessages` HumanMessage instances
export function createTrimMessagesReducer(maxUserMessages: number) {
	return (current: BaseMessage[]): BaseMessage[] => {
		// Count HumanMessage instances and remember their indices
		const humanMessageIndices: number[] = [];
		current.forEach((msg, index) => {
			if (msg instanceof HumanMessage) {
				humanMessageIndices.push(index);
			}
		});

		// If we have fewer than or equal to maxUserMessages, return as is
		if (humanMessageIndices.length <= maxUserMessages) {
			return current;
		}

		// Find the index of the first HumanMessage that we want to keep
		const startHumanMessageIndex =
			humanMessageIndices[humanMessageIndices.length - maxUserMessages];

		// Slice from that HumanMessage onwards
		return current.slice(startHumanMessageIndex);
	};
}

export const WorkflowState = Annotation.Root({
	messages: Annotation<BaseMessage[]>({
		reducer: messagesStateReducer,
		default: () => [],
	}),
	// // The original prompt from the user.
	// The JSON representation of the workflow being built.
	// Now a simple field without custom reducer - all updates go through operations
	workflowJSON: Annotation<SimpleWorkflow>({
		reducer: (x, y) => y ?? x,
		default: () => ({ nodes: [], connections: {}, name: '' }),
	}),
	// Operations to apply to the workflow - processed by a separate node
	workflowOperations: Annotation<WorkflowOperation[] | null>({
		reducer: operationsReducer,
		default: () => [],
	}),
	// Latest workflow context
	workflowContext: Annotation<ChatPayload['workflowContext'] | undefined>({
		reducer: (x, y) => y ?? x,
	}),
	// Results of last workflow validation
	workflowValidation: Annotation<ProgrammaticEvaluationResult | null>({
		reducer: (x, y) => (y === undefined ? x : y),
		default: () => null,
	}),
	// Compacted programmatic validations history for telemetry
	validationHistory: Annotation<TelemetryValidationStatus[]>({
		reducer: (x, y) => (y && y.length > 0 ? [...x, ...y] : x),
		default: () => [],
	}),
	// Technique categories identified from categorize_prompt tool for telemetry
	techniqueCategories: Annotation<string[]>({
		reducer: (x, y) => (y && y.length > 0 ? [...x, ...y] : x),
		default: () => [],
	}),

	// Previous conversation summary (used for compressing long conversations)
	previousSummary: Annotation<string>({
		reducer: (x, y) => y ?? x, // Overwrite with the latest summary
		default: () => 'EMPTY',
	}),

	// Template IDs fetched from workflow examples for telemetry
	templateIds: Annotation<number[]>({
		reducer: appendArrayReducer,
		default: () => [],
	}),

	// Cached workflow templates from template API
	// Shared across tools to reduce API calls
	cachedTemplates: Annotation<WorkflowMetadata[]>({
		reducer: cachedTemplatesReducer,
		default: () => [],
	}),
});
