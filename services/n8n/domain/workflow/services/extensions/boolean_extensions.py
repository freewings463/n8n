"""
MIGRATION-META:
  source_path: packages/workflow/src/extensions/boolean-extensions.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/extensions 的工作流模块。导入/依赖:外部:无；内部:无；本地:./extensions。导出:toBoolean、toInt、toDateTime、booleanExtensions。关键函数/方法:toBoolean、toInt、toDateTime。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/extensions/boolean-extensions.ts -> services/n8n/domain/workflow/services/extensions/boolean_extensions.py

import type { Extension, ExtensionMap } from './extensions';

export function toBoolean(value: boolean) {
	return value;
}

export function toInt(value: boolean) {
	return value ? 1 : 0;
}

export function toDateTime() {
	return undefined;
}

const toFloat = toInt;
const toNumber: Extension = toInt.bind({});

toNumber.doc = {
	name: 'toNumber',
	description:
		'Converts <code>true</code> to <code>1</code> and <code>false</code> to <code>0</code>.',
	examples: [
		{ example: 'true.toNumber()', evaluated: '1' },
		{ example: 'false.toNumber()', evaluated: '0' },
	],
	section: 'cast',
	returnType: 'number',
	docURL:
		'https://docs.n8n.io/code/builtin/data-transformation-functions/booleans/#boolean-toNumber',
};

export const booleanExtensions: ExtensionMap = {
	typeName: 'Boolean',
	functions: {
		toBoolean,
		toInt,
		toFloat,
		toNumber,
		toDateTime,
	},
};
