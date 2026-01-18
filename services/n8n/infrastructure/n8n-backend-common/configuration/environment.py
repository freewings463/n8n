"""
MIGRATION-META:
  source_path: packages/@n8n/backend-common/src/environment.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/backend-common/src 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:inTest、inProduction、inDevelopment。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/backend-common treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/backend-common/src/environment.ts -> services/n8n/infrastructure/n8n-backend-common/configuration/environment.py

const { NODE_ENV } = process.env;

export const inTest = NODE_ENV === 'test';
export const inProduction = NODE_ENV === 'production';
export const inDevelopment = !NODE_ENV || NODE_ENV === 'development';
