"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/js-task-runner/errors/error-like.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src/js-task-runner/errors 的错误。导入/依赖:外部:无；内部:无；本地:无。导出:ErrorLike、isErrorLike。关键函数/方法:isErrorLike。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Task runner process runtime -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/js-task-runner/errors/error-like.ts -> services/n8n/infrastructure/n8n-task-runner/container/js-task-runner/errors/error_like.py

export interface ErrorLike {
	message: string;
	stack?: string;
}

export function isErrorLike(value: unknown): value is ErrorLike {
	if (typeof value !== 'object' || value === null) return false;

	const errorLike = value as ErrorLike;

	return typeof errorLike.message === 'string';
}
