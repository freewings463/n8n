"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/parsers/parse-enum.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/parsers 的模块。导入/依赖:外部:zod；内部:无；本地:../types。导出:parseEnum。关键函数/方法:parseEnum。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/parsers/parse-enum.ts -> services/n8n/application/n8n-json-schema-to-zod/services/parsers/parse_enum.py

import { z } from 'zod';

import type { JsonSchemaObject, Serializable } from '../types';

export const parseEnum = (jsonSchema: JsonSchemaObject & { enum: Serializable[] }) => {
	if (jsonSchema.enum.length === 0) {
		return z.never();
	}

	if (jsonSchema.enum.length === 1) {
		// union does not work when there is only one element
		return z.literal(jsonSchema.enum[0] as z.Primitive);
	}

	if (jsonSchema.enum.every((x) => typeof x === 'string')) {
		return z.enum(jsonSchema.enum as [string]);
	}

	return z.union(
		jsonSchema.enum.map((x) => z.literal(x as z.Primitive)) as unknown as [
			z.ZodTypeAny,
			z.ZodTypeAny,
		],
	);
};
