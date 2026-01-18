"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/helpers/progress.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools/helpers 的工作流模块。导入/依赖:外部:@langchain/core/tools、@langchain/langgraph；内部:无；本地:无。导出:createProgressReporter、reportStart、reportProgress、reportComplete、reportError、createBatchProgressReporter。关键函数/方法:emit、progress、error、createBatchReporter、reportProgress、reportError、createBatchProgressReporter。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/helpers/progress.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/tools/helpers/progress.py

import type { ToolRunnableConfig } from '@langchain/core/tools';
import type { LangGraphRunnableConfig } from '@langchain/langgraph';

import type {
	ToolProgressMessage,
	ToolError,
	ProgressReporter,
	BatchReporter,
} from '../../types/tools';

/**
 * Create a progress reporter for a tool execution
 *
 * @param config
 * @param toolName
 * @param displayTitle the general tool action name, for example "Searching for nodes"
 * @param customTitle custom title per tool call, for example "Searching for OpenAI"
 */
export function createProgressReporter<TToolName extends string = string>(
	config: ToolRunnableConfig & LangGraphRunnableConfig,
	toolName: TToolName,
	displayTitle: string,
	customTitle?: string,
): ProgressReporter {
	const toolCallId = config.toolCall?.id;

	let customDisplayTitle = customTitle;

	const emit = (message: ToolProgressMessage<TToolName>): void => {
		config.writer?.(message);
	};

	const start = <T>(input: T, options?: { customDisplayTitle: string }): void => {
		if (options?.customDisplayTitle) {
			customDisplayTitle = options.customDisplayTitle;
		}
		emit({
			type: 'tool',
			toolName,
			toolCallId,
			displayTitle,
			customDisplayTitle,
			status: 'running',
			updates: [
				{
					type: 'input',
					data: input as Record<string, unknown>,
				},
			],
		});
	};

	const progress = (message: string, data?: Record<string, unknown>): void => {
		emit({
			type: 'tool',
			toolName,
			toolCallId,
			displayTitle,
			customDisplayTitle,
			status: 'running',
			updates: [
				{
					type: 'progress',
					data: data ?? { message },
				},
			],
		});
	};

	const complete = <T>(output: T): void => {
		emit({
			type: 'tool',
			toolName,
			toolCallId,
			displayTitle,
			customDisplayTitle,
			status: 'completed',
			updates: [
				{
					type: 'output',
					data: output as Record<string, unknown>,
				},
			],
		});
	};

	const error = (error: ToolError): void => {
		emit({
			type: 'tool',
			toolName,
			toolCallId,
			displayTitle,
			customDisplayTitle,
			status: 'error',
			updates: [
				{
					type: 'error',
					data: {
						message: error.message,
						code: error.code,
						details: error.details,
					},
				},
			],
		});
	};

	const createBatchReporter = (scope: string): BatchReporter => {
		let currentIndex = 0;
		let totalItems = 0;

		return {
			init: (total: number) => {
				totalItems = total;
				currentIndex = 0;
			},
			next: (itemDescription: string) => {
				currentIndex++;
				progress(`${scope}: Processing item ${currentIndex} of ${totalItems}: ${itemDescription}`);
			},
			complete: () => {
				progress(`${scope}: Completed all ${totalItems} items`);
			},
		};
	};

	return {
		start,
		progress,
		complete,
		error,
		createBatchReporter,
	};
}

/**
 * Helper function to report start of tool execution
 */
export function reportStart<T>(reporter: ProgressReporter, input: T): void {
	reporter.start(input);
}

/**
 * Helper function to report progress during tool execution
 */
export function reportProgress(
	reporter: ProgressReporter,
	message: string,
	data?: Record<string, unknown>,
): void {
	reporter.progress(message, data);
}

/**
 * Helper function to report successful completion
 */
export function reportComplete<T>(reporter: ProgressReporter, output: T): void {
	reporter.complete(output);
}

/**
 * Helper function to report error during execution
 */
export function reportError(reporter: ProgressReporter, error: ToolError): void {
	reporter.error(error);
}

/**
 * Create a batch progress reporter for multi-item operations
 */
export function createBatchProgressReporter(
	reporter: ProgressReporter,
	scope: string,
): BatchReporter {
	return reporter.createBatchReporter(scope);
}
