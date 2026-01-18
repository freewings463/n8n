"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/js-task-runner/errors/execution-error.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src/js-task-runner/errors 的执行错误。导入/依赖:外部:无；内部:无；本地:./error-like、./serializable-error。导出:ExecutionError。关键函数/方法:populateFromStack、stackRows、toLineNumberDisplay、toErrorDetailsAndType。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Task runner process runtime -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/js-task-runner/errors/execution-error.ts -> services/n8n/infrastructure/n8n-task-runner/container/js-task-runner/errors/execution_error.py

import type { ErrorLike } from './error-like';
import { SerializableError } from './serializable-error';

export class ExecutionError extends SerializableError {
	description: string | null = null;

	itemIndex: number | undefined = undefined;

	context: { itemIndex: number } | undefined = undefined;

	lineNumber: number | undefined = undefined;

	constructor(error: ErrorLike, itemIndex?: number) {
		super(error.message);
		this.itemIndex = itemIndex;

		if (this.itemIndex !== undefined) {
			this.context = { itemIndex: this.itemIndex };
		}

		// Override the stack trace with the given error's stack trace. Since
		// node v22 it's not writable, so we can't assign it directly
		Object.defineProperty(this, 'stack', {
			value: error.stack,
			enumerable: true,
		});

		this.populateFromStack();
	}

	/**
	 * Populate error `message` and `description` from error `stack`.
	 */
	private populateFromStack() {
		const stackRows = (this.stack ?? '').split('\n');

		if (stackRows.length === 0) {
			this.message = 'Unknown error';
			return;
		}

		const messageRow = stackRows.find((line) => line.includes('Error:'));
		const lineNumberDisplay = this.toLineNumberDisplay(stackRows);

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

		this.message = `${errorDetails} ${lineNumberDisplay}`;
	}

	private toLineNumberDisplay(stackRows: string[]) {
		if (!stackRows || stackRows.length === 0) return '';

		const userFnLine = stackRows.find(
			(row) => row.match(/\(evalmachine\.<anonymous>:\d+:\d+\)/) && !row.includes('VmCodeWrapper'),
		);

		if (userFnLine) {
			const match = userFnLine.match(/evalmachine\.<anonymous>:(\d+):/);
			if (match) this.lineNumber = Number(match[1]);
		}

		if (this.lineNumber === undefined) {
			const topLevelLine = stackRows.find(
				(row) => row.includes('VmCodeWrapper') && row.includes('evalmachine.<anonymous>'),
			);

			if (topLevelLine) {
				const match = topLevelLine.match(/evalmachine\.<anonymous>:(\d+):/);
				if (match) this.lineNumber = Number(match[1]);
			}
		}

		if (this.lineNumber === undefined) return '';

		return this.itemIndex === undefined
			? `[line ${this.lineNumber}]`
			: `[line ${this.lineNumber}, for item ${this.itemIndex}]`;
	}

	private toErrorDetailsAndType(messageRow?: string) {
		if (!messageRow) return [null, null];

		const segments = messageRow.split(':').map((i) => i.trim());
		if (segments[1] === "Cannot find module 'node") {
			segments[1] = `${segments[1]}:${segments[2]}`;
			segments.splice(2, 1);
		}

		if (
			segments.length >= 3 &&
			segments[1]?.startsWith("Module 'node") &&
			segments[2]?.includes("' is disallowed")
		) {
			segments[1] = `${segments[1]}:${segments[2]}`;
			segments.splice(2, 1);
		}

		const [errorDetails, errorType] = segments.reverse();
		return [errorDetails, errorType === 'Error' ? null : errorType];
	}
}
