"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src 的入口。导入/依赖:外部:无；内部:无；本地:无。导出:jsonSchemaToZod。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/index.ts -> services/n8n/application/n8n-json-schema-to-zod/services/__init__.py

export type * from './types';
export { jsonSchemaToZod } from './json-schema-to-zod';
