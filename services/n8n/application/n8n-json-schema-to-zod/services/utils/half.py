"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/utils/half.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:half。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/utils/half.ts -> services/n8n/application/n8n-json-schema-to-zod/services/utils/half.py

export const half = <T>(arr: T[]): [T[], T[]] => {
	return [arr.slice(0, arr.length / 2), arr.slice(arr.length / 2)];
};
