"""
MIGRATION-META:
  source_path: packages/workflow/src/extensions/utils.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/extensions 的工作流模块。导入/依赖:外部:luxon；内部:无；本地:../errors/expression-extension.error。导出:convertToDateTime、checkIfValueDefinedOrThrow。关键函数/方法:convertToDateTime。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/extensions/utils.ts -> services/n8n/domain/workflow/services/extensions/utils.py

import { DateTime } from 'luxon';

import { ExpressionExtensionError } from '../errors/expression-extension.error';

// Utility functions and type guards for expression extensions

export const convertToDateTime = (value: string | Date | DateTime): DateTime | undefined => {
	let converted: DateTime | undefined;

	if (typeof value === 'string') {
		converted = DateTime.fromJSDate(new Date(value));
		if (converted.invalidReason !== null) {
			return;
		}
	} else if (value instanceof Date) {
		converted = DateTime.fromJSDate(value);
	} else if (DateTime.isDateTime(value)) {
		converted = value;
	}
	return converted;
};

export function checkIfValueDefinedOrThrow<T>(value: T, functionName: string): void {
	if (value === undefined || value === null) {
		throw new ExpressionExtensionError(`${functionName} can't be used on ${String(value)} value`, {
			description: `To ignore this error, add a ? to the variable before this function, e.g. my_var?.${functionName}`,
		});
	}
}
