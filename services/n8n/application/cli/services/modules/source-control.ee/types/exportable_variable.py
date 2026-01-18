"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/types/exportable-variable.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/source-control.ee/types 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:ExportableVariable。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/types/exportable-variable.ts -> services/n8n/application/cli/services/modules/source-control.ee/types/exportable_variable.py

export interface ExportableVariable {
	id: string;
	key: string;
	type: string;
	value: string;
	projectId?: string;
}
