"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/utils/size-utils.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/data-table/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:toMb、formatBytes。关键函数/方法:toMb、formatBytes。用于提供该模块通用工具能力（纯函数/封装器）供复用。注释目标:Convert bytes to megabytes (rounded to nearest integer)。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/utils/size-utils.ts -> services/n8n/application/cli/services/modules/data-table/utils/size_utils.py

/**
 * Convert bytes to megabytes (rounded to nearest integer)
 */
export function toMb(sizeInBytes: number): number {
	return Math.round(sizeInBytes / (1024 * 1024));
}

/**
 * Format bytes to human-readable size with appropriate unit (B, KB, or MB)
 */
export function formatBytes(sizeInBytes: number): string {
	if (sizeInBytes < 1024) {
		return `${sizeInBytes}B`;
	} else if (sizeInBytes < 1024 * 1024) {
		return `${Math.round(sizeInBytes / 1024)}KB`;
	} else {
		return `${Math.round(sizeInBytes / (1024 * 1024))}MB`;
	}
}
