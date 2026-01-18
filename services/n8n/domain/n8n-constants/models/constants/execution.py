"""
MIGRATION-META:
  source_path: packages/@n8n/constants/src/execution.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/constants/src 的执行模块。导入/依赖:外部:无；内部:无；本地:无。导出:TOOL_EXECUTOR_NODE_NAME。关键函数/方法:无。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/constants treated as domain constants
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/constants/src/execution.ts -> services/n8n/domain/n8n-constants/models/constants/execution.py

export const TOOL_EXECUTOR_NODE_NAME = 'PartialExecutionToolExecutor';
