"""
MIGRATION-META:
  source_path: packages/cli/src/modules/insights/database/entities/insights-shared.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/insights/database 的Insights模块。导入/依赖:外部:无；内部:无；本地:无。导出:PeriodUnitToNumber、PeriodUnit、PeriodUnitNumber、NumberToPeriodUnit、isValidPeriodNumber、TypeToNumber、TypeUnit、TypeUnitNumber 等2项。关键函数/方法:isValidPeriodNumber、isValidTypeNumber。用于承载Insights实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/insights/database/entities/insights-shared.ts -> services/n8n/application/cli/services/modules/insights/database/entities/insights_shared.py

function isValid<T extends Record<number | string | symbol, unknown>>(
	value: number | string | symbol,
	constant: T,
): value is keyof T {
	return Object.keys(constant).includes(value.toString());
}

// Periods
export const PeriodUnitToNumber = {
	hour: 0,
	day: 1,
	week: 2,
} as const;

export type PeriodUnit = keyof typeof PeriodUnitToNumber;

export type PeriodUnitNumber = (typeof PeriodUnitToNumber)[PeriodUnit];
export const NumberToPeriodUnit = Object.entries(PeriodUnitToNumber).reduce(
	(acc, [key, value]: [PeriodUnit, PeriodUnitNumber]) => {
		acc[value] = key;
		return acc;
	},
	{} as Record<PeriodUnitNumber, PeriodUnit>,
);
export function isValidPeriodNumber(value: number) {
	return isValid(value, NumberToPeriodUnit);
}

// Types
export const TypeToNumber = {
	time_saved_min: 0,
	runtime_ms: 1,
	success: 2,
	failure: 3,
} as const;

export type TypeUnit = keyof typeof TypeToNumber;

export type TypeUnitNumber = (typeof TypeToNumber)[TypeUnit];
export const NumberToType = Object.entries(TypeToNumber).reduce(
	(acc, [key, value]: [TypeUnit, TypeUnitNumber]) => {
		acc[value] = key;
		return acc;
	},
	{} as Record<TypeUnitNumber, TypeUnit>,
);

export function isValidTypeNumber(value: number) {
	return isValid(value, NumberToType);
}
