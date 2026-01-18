"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/parsers/parse-all-of.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/parsers 的模块。导入/依赖:外部:zod；内部:无；本地:./parse-schema、../types、../utils/half。导出:parseAllOf。关键函数/方法:ensureOriginalIndex、parseAllOf。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/parsers/parse-all-of.ts -> services/n8n/application/n8n-json-schema-to-zod/services/parsers/parse_all_of.py

import { z } from 'zod';

import { parseSchema } from './parse-schema';
import type { JsonSchemaObject, JsonSchema, Refs } from '../types';
import { half } from '../utils/half';

const originalIndex = Symbol('Original index');

const ensureOriginalIndex = (arr: JsonSchema[]) => {
	const newArr = [];

	for (let i = 0; i < arr.length; i++) {
		const item = arr[i];
		if (typeof item === 'boolean') {
			newArr.push(item ? { [originalIndex]: i } : { [originalIndex]: i, not: {} });
		} else if (originalIndex in item) {
			return arr;
		} else {
			newArr.push({ ...item, [originalIndex]: i });
		}
	}

	return newArr;
};

export function parseAllOf(
	jsonSchema: JsonSchemaObject & { allOf: JsonSchema[] },
	refs: Refs,
): z.ZodTypeAny {
	if (jsonSchema.allOf.length === 0) {
		return z.never();
	}

	if (jsonSchema.allOf.length === 1) {
		const item = jsonSchema.allOf[0];

		return parseSchema(item, {
			...refs,
			path: [...refs.path, 'allOf', (item as never)[originalIndex]],
		});
	}

	const [left, right] = half(ensureOriginalIndex(jsonSchema.allOf));

	return z.intersection(parseAllOf({ allOf: left }, refs), parseAllOf({ allOf: right }, refs));
}
