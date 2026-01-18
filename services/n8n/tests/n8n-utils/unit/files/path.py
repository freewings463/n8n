"""
MIGRATION-META:
  source_path: packages/@n8n/utils/src/files/path.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/utils/src/files 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:isWindowsFilePath。关键函数/方法:isWindowsFilePath。用于提供该模块通用工具能力（纯函数/封装器）供复用。注释目标:Fast check if file path starts with a windows drive letter, e.g. 'C:/' or 'C:\\'。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/utils/src/files/path.ts -> services/n8n/tests/n8n-utils/unit/files/path.py

/**
 * Fast check if file path starts with a windows drive letter, e.g. 'C:/' or 'C:\\'
 */
export function isWindowsFilePath(str: string) {
	return /^[a-zA-Z]:[\\/]/.test(str);
}
