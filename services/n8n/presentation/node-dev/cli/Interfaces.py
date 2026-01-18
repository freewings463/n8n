"""
MIGRATION-META:
  source_path: packages/node-dev/src/Interfaces.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/node-dev/src 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:IBuildOptions。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-dev CLI tool -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/node-dev/src/Interfaces.ts -> services/n8n/presentation/node-dev/cli/Interfaces.py

export interface IBuildOptions {
	destinationFolder?: string;
	watch?: boolean;
}
