"""
MIGRATION-META:
  source_path: packages/@n8n/utils/src/sort/sortByProperty.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/utils/src/sort 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:sortByProperty。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Generic shared utilities -> application/services/utils
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/utils/src/sort/sortByProperty.ts -> services/n8n/application/n8n-utils/services/utils/sort/sortByProperty.py

export const sortByProperty = <T>(
	property: keyof T,
	arr: T[],
	order: 'asc' | 'desc' = 'asc',
): T[] =>
	arr.sort((a, b) => {
		const result = String(a[property]).localeCompare(String(b[property]), undefined, {
			numeric: true,
			sensitivity: 'base',
		});
		return order === 'asc' ? result : -result;
	});
