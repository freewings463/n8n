"""
MIGRATION-META:
  source_path: packages/workflow/src/result.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流模块。导入/依赖:外部:无；内部:无；本地:./errors。导出:ResultOk、ResultError、Result、createResultOk、createResultError、toResult。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/result.ts -> services/n8n/domain/workflow/services/result.py

import { ensureError } from './errors';

export type ResultOk<T> = { ok: true; result: T };
export type ResultError<E> = { ok: false; error: E };
export type Result<T, E> = ResultOk<T> | ResultError<E>;

export const createResultOk = <T>(data: T): ResultOk<T> => ({
	ok: true,
	result: data,
});

export const createResultError = <E = unknown>(error: E): ResultError<E> => ({
	ok: false,
	error,
});

/**
 * Executes the given function and converts it to a Result object.
 *
 * @example
 * const result = toResult(() => fs.writeFileSync('file.txt', 'Hello, World!'));
 */
export const toResult = <T, E extends Error = Error>(fn: () => T): Result<T, E> => {
	try {
		return createResultOk<T>(fn());
	} catch (e) {
		const error = ensureError(e);
		return createResultError<E>(error as E);
	}
};
