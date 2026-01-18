"""
MIGRATION-META:
  source_path: packages/workflow/src/extensions/extended-functions.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/extensions 的工作流模块。导入/依赖:外部:无；内部:无；本地:./array-extensions、../errors/expression-extension.error、../errors/expression.error。导出:extendedFunctions。关键函数/方法:numberList、zip、average、not。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/extensions/extended-functions.ts -> services/n8n/domain/workflow/services/extensions/extended_functions.py

import { average as aAverage } from './array-extensions';
import { ExpressionExtensionError } from '../errors/expression-extension.error';
import { ExpressionError } from '../errors/expression.error';

const min = Math.min;
const max = Math.max;

const numberList = (start: number, end: number): number[] => {
	const size = Math.abs(start - end) + 1;
	const arr = new Array<number>(size);

	let curr = start;
	for (let i = 0; i < size; i++) {
		if (start < end) {
			arr[i] = curr++;
		} else {
			arr[i] = curr--;
		}
	}

	return arr;
};

const zip = (keys: unknown[], values: unknown[]): unknown => {
	if (keys.length !== values.length) {
		throw new ExpressionExtensionError('keys and values not of equal length');
	}
	return keys.reduce((p, c, i) => {
		// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-explicit-any
		(p as any)[c as any] = values[i];
		return p;
	}, {});
};

const average = (...args: number[]) => {
	return aAverage(args);
};

const not = (value: unknown): boolean => {
	return !value;
};

function ifEmpty<T, V>(value: V, defaultValue: T) {
	if (arguments.length !== 2) {
		throw new ExpressionError('expected two arguments (value, defaultValue) for this function');
	}
	if (value === undefined || value === null || value === '') {
		return defaultValue;
	}
	if (typeof value === 'object') {
		if (Array.isArray(value) && !value.length) {
			return defaultValue;
		}
		if (!Object.keys(value).length) {
			return defaultValue;
		}
	}
	return value;
}

ifEmpty.doc = {
	name: 'ifEmpty',
	description:
		'Returns the default value if the value is empty. Empty values are undefined, null, empty strings, arrays without elements and objects without keys.',
	returnType: 'any',
	args: [
		{ name: 'value', type: 'any' },
		{ name: 'defaultValue', type: 'any' },
	],
	docURL: 'https://docs.n8n.io/code/builtin/convenience',
};

export const extendedFunctions = {
	min,
	max,
	not,
	average,
	numberList,
	zip,
	$min: min,
	$max: max,
	$average: average,
	$not: not,
	$ifEmpty: ifEmpty,
};
