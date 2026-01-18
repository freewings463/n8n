"""
MIGRATION-META:
  source_path: packages/@n8n/errors/src/index.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/errors/src 的入口。导入/依赖:外部:无；内部:无；本地:无。导出:ApplicationError。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Shared error types -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/errors/src/index.ts -> services/n8n/domain/n8n-errors/exceptions/__init__.py

export { ApplicationError } from './application.error';
export type * from './types';
