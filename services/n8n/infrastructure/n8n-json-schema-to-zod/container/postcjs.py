"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/postcjs.cjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/json-schema-to-zod 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:require。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/postcjs.cjs -> services/n8n/infrastructure/n8n-json-schema-to-zod/container/postcjs.py

require('fs').writeFileSync('./dist/cjs/package.json', '{"type":"commonjs"}', 'utf-8');
