"""
MIGRATION-META:
  source_path: packages/workflow/src/deferred-promise.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流模块。导入/依赖:外部:无；内部:无；本地:无。导出:IDeferredPromise、createDeferredPromise。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/deferred-promise.ts -> services/n8n/domain/workflow/services/deferred_promise.py

type ResolveFn<T> = (result: T | PromiseLike<T>) => void;
type RejectFn = (error: Error) => void;

export interface IDeferredPromise<T> {
	promise: Promise<T>;
	resolve: ResolveFn<T>;
	reject: RejectFn;
}

export function createDeferredPromise<T = void>(): IDeferredPromise<T> {
	const deferred: Partial<IDeferredPromise<T>> = {};
	deferred.promise = new Promise<T>((resolve, reject) => {
		deferred.resolve = resolve;
		deferred.reject = reject;
	});
	return deferred as IDeferredPromise<T>;
}
