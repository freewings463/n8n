"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/js-task-runner/obj-utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src/js-task-runner 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:isObject。关键函数/方法:isObject。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Task runner process runtime -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/js-task-runner/obj-utils.ts -> services/n8n/infrastructure/n8n-task-runner/container/js-task-runner/obj_utils.py

export function isObject(maybe: unknown): maybe is object {
	return (
		typeof maybe === 'object' && maybe !== null && !Array.isArray(maybe) && !(maybe instanceof Date)
	);
}
