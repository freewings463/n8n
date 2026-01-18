"""
MIGRATION-META:
  source_path: packages/@n8n/constants/src/time.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/constants/src 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:Time。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:Convert time from any time unit to any other unit。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/constants treated as domain constants
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/constants/src/time.ts -> services/n8n/domain/n8n-constants/models/constants/time.py

/**
 * Convert time from any time unit to any other unit
 */
export const Time = {
	milliseconds: {
		toHours: 1 / (60 * 60 * 1000),
		toMinutes: 1 / (60 * 1000),
		toSeconds: 1 / 1000,
	},
	seconds: {
		toMilliseconds: 1000,
	},
	minutes: {
		toMilliseconds: 60 * 1000,
	},
	hours: {
		toMilliseconds: 60 * 60 * 1000,
		toSeconds: 60 * 60,
	},
	days: {
		toSeconds: 24 * 60 * 60,
		toMilliseconds: 24 * 60 * 60 * 1000,
	},
};
