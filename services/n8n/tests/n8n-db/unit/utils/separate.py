"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/separate.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:separate。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/separate.ts -> services/n8n/tests/n8n-db/unit/utils/separate.py

export const separate = <T>(array: T[], test: (element: T) => boolean) => {
	const pass: T[] = [];
	const fail: T[] = [];

	array.forEach((i) => (test(i) ? pass : fail).push(i));

	return [pass, fail];
};
