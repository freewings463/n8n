"""
MIGRATION-META:
  source_path: packages/core/src/nodes-loader/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/nodes-loader 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:PackageJson。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node loading/discovery -> infrastructure/container/nodes_loader
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/nodes-loader/types.ts -> services/n8n/infrastructure/core/container/nodes_loader/types.py

export namespace n8n {
	export interface PackageJson {
		name: string;
		version: string;
		n8n?: {
			credentials?: string[];
			nodes?: string[];
		};
		author?: {
			name?: string;
			email?: string;
		};
	}
}
