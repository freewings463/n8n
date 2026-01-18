"""
MIGRATION-META:
  source_path: packages/workflow/src/errors/execution-cancelled.error.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/errors 的工作流错误。导入/依赖:外部:无；内部:无；本地:./abstract/execution-base.error。导出:CancellationReason、ManualExecutionCancelledError、TimeoutExecutionCancelledError、SystemShutdownExecutionCancelledError。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Workflow errors -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/errors/execution-cancelled.error.ts -> services/n8n/domain/workflow/exceptions/execution_cancelled_error.py

import { ExecutionBaseError } from './abstract/execution-base.error';

export type CancellationReason = 'manual' | 'timeout' | 'shutdown';

export abstract class ExecutionCancelledError extends ExecutionBaseError {
	readonly reason: CancellationReason;

	// NOTE: prefer one of the more specific
	constructor(executionId: string, reason: CancellationReason) {
		super('The execution was cancelled', {
			level: 'warning',
			extra: { executionId },
		});
		this.reason = reason;
	}
}

export class ManualExecutionCancelledError extends ExecutionCancelledError {
	constructor(executionId: string) {
		super(executionId, 'manual');
		this.message = 'The execution was cancelled manually';
	}
}

export class TimeoutExecutionCancelledError extends ExecutionCancelledError {
	constructor(executionId: string) {
		super(executionId, 'timeout');
		this.message = 'The execution was cancelled because it timed out';
	}
}

export class SystemShutdownExecutionCancelledError extends ExecutionCancelledError {
	constructor(executionId: string) {
		super(executionId, 'shutdown');
		this.message = 'The execution was cancelled because the system is shutting down';
	}
}
