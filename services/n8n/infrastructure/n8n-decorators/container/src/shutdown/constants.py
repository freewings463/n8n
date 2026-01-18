"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/shutdown/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/shutdown 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:LOWEST_SHUTDOWN_PRIORITY、DEFAULT_SHUTDOWN_PRIORITY、HIGHEST_SHUTDOWN_PRIORITY。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/shutdown/constants.ts -> services/n8n/infrastructure/n8n-decorators/container/src/shutdown/constants.py

export const LOWEST_SHUTDOWN_PRIORITY = 0;
export const DEFAULT_SHUTDOWN_PRIORITY = 100;
export const HIGHEST_SHUTDOWN_PRIORITY = 200;
