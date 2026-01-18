"""
MIGRATION-META:
  source_path: packages/cli/src/modules/insights/insights.constants.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/insights 的Insights模块。导入/依赖:外部:无；内部:无；本地:无。导出:INSIGHTS_DATE_RANGE_KEYS、keyRangeToDays。关键函数/方法:无。用于承载Insights实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/insights/insights.constants.ts -> services/n8n/application/cli/services/modules/insights/insights_constants.py

export const INSIGHTS_DATE_RANGE_KEYS = [
	'day',
	'week',
	'2weeks',
	'month',
	'quarter',
	'6months',
	'year',
] as const;

export const keyRangeToDays: Record<(typeof INSIGHTS_DATE_RANGE_KEYS)[number], number> = {
	day: 1,
	week: 7,
	'2weeks': 14,
	month: 30,
	quarter: 90,
	'6months': 180,
	year: 365,
};
