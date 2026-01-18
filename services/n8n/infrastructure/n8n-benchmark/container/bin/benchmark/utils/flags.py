"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/scripts/utils/flags.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/scripts/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:flagsObjectToCliArgs。关键函数/方法:flagsObjectToCliArgs。用于提供该模块通用工具能力（纯函数/封装器）供复用。注释目标:@ts-check。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark scripts -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/scripts/utils/flags.mjs -> services/n8n/infrastructure/n8n-benchmark/container/bin/benchmark/utils/flags.py

// @ts-check

/**
 * Converts an object of flags to an array of CLI arguments.
 *
 * @param {Record<string, string | undefined>} flags
 *
 * @returns {string[]}
 */
export function flagsObjectToCliArgs(flags) {
	return Object.entries(flags)
		.filter(([, value]) => value !== undefined)
		.map(([key, value]) => {
			if (typeof value === 'string' && value.includes(' ')) {
				return `--${key}="${value}"`;
			} else {
				return `--${key}=${value}`;
			}
		});
}
