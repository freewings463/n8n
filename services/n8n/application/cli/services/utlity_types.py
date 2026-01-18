"""
MIGRATION-META:
  source_path: packages/cli/src/utlity.types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:Resolve。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。注释目标:Display an intersection type without implementation details.。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/utlity.types.ts -> services/n8n/application/cli/services/utlity_types.py

/**
 * Display an intersection type without implementation details.
 * @doc https://effectivetypescript.com/2022/02/25/gentips-4-display/
 */
// eslint-disable-next-line @typescript-eslint/no-restricted-types
export type Resolve<T> = T extends Function ? T : { [K in keyof T]: T[K] };
