"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Code/ExecutionError.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Code 的执行节点。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:ExecutionError。关键函数/方法:populateFromStack、toLineNumberDisplay、toErrorDetailsAndType。用于实现 n8n 执行节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Code/ExecutionError.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Code/ExecutionError.py

import { ApplicationError } from '@n8n/errors';

export class ExecutionError extends ApplicationError {
	description: string | null = null;

	itemIndex: number | undefined = undefined;

	context: { itemIndex: number } | undefined = undefined;

	stack = '';

	lineNumber: number | undefined = undefined;

	constructor(error: Error & { stack?: string }, itemIndex?: number) {
		super(error.message);
		this.itemIndex = itemIndex;

		if (this.itemIndex !== undefined) {
			this.context = { itemIndex: this.itemIndex };
		}

		this.stack = error.stack ?? '';

		this.populateFromStack();
	}

	/**
	 * Populate error `message` and `description` from error `stack`.
	 */
	private populateFromStack() {
		const stackRows = this.stack && typeof this.stack === 'string' ? this.stack.split('\n') : [];

		if (stackRows.length === 0) {
			this.message = 'Unknown error';
			return;
		}

		const messageRow = stackRows.find((line) => line.includes('Error:'));
		const lineNumberRow = stackRows.find((line) => line.includes('Code:'));
		const lineNumberDisplay = this.toLineNumberDisplay(lineNumberRow) || '';

		if (!messageRow) {
			this.message = `Unknown error ${lineNumberDisplay}`;
			return;
		}

		const [errorDetails, errorType] = this.toErrorDetailsAndType(messageRow);

		if (errorType) this.description = errorType;

		if (!errorDetails) {
			this.message = `Unknown error ${lineNumberDisplay}`;
			return;
		}

		this.message = `${errorDetails} ${lineNumberDisplay}`.trim();
	}

	private toLineNumberDisplay(lineNumberRow?: string) {
		const errorLineNumberMatch = lineNumberRow?.match(/Code:(?<lineNumber>\d+)/);

		if (!errorLineNumberMatch?.groups?.lineNumber) return null;

		const lineNumber = errorLineNumberMatch.groups.lineNumber;

		this.lineNumber = Number(lineNumber);

		if (!lineNumber) return '';

		return this.itemIndex === undefined
			? `[line ${lineNumber}]`
			: `[line ${lineNumber}, for item ${this.itemIndex}]`;
	}

	private toErrorDetailsAndType(messageRow?: string) {
		if (!messageRow) return [null, null];

		// Remove "Error: " prefix added by stacktrace formatting
		messageRow = messageRow.replace(/^Error: /, '');

		const colonIndex = messageRow.indexOf(': ');
		if (colonIndex === -1) {
			return [messageRow.trim(), null];
		}

		const errorType = messageRow.substring(0, colonIndex).trim();
		const errorDetails = messageRow.substring(colonIndex + 2).trim();

		return [errorDetails, errorType === 'Error' ? null : errorType];
	}
}
