"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/parsers/parse-string.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/parsers 的模块。导入/依赖:外部:zod；内部:无；本地:../types、../utils/extend-schema。导出:parseString。关键函数/方法:parseString。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/parsers/parse-string.ts -> services/n8n/application/n8n-json-schema-to-zod/services/parsers/parse_string.py

import { z } from 'zod';

import type { JsonSchemaObject } from '../types';
import { extendSchemaWithMessage } from '../utils/extend-schema';

export const parseString = (jsonSchema: JsonSchemaObject & { type: 'string' }) => {
	let zodSchema = z.string();

	zodSchema = extendSchemaWithMessage(zodSchema, jsonSchema, 'format', (zs, format, errorMsg) => {
		switch (format) {
			case 'email':
				return zs.email(errorMsg);
			case 'ip':
				return zs.ip(errorMsg);
			case 'ipv4':
				return zs.ip({ version: 'v4', message: errorMsg });
			case 'ipv6':
				return zs.ip({ version: 'v6', message: errorMsg });
			case 'uri':
				return zs.url(errorMsg);
			case 'uuid':
				return zs.uuid(errorMsg);
			case 'date-time':
				return zs.datetime({ offset: true, message: errorMsg });
			case 'time':
				return zs.time(errorMsg);
			case 'date':
				return zs.date(errorMsg);
			case 'binary':
				return zs.base64(errorMsg);
			case 'duration':
				return zs.duration(errorMsg);
			default:
				return zs;
		}
	});

	zodSchema = extendSchemaWithMessage(zodSchema, jsonSchema, 'contentEncoding', (zs, _, errorMsg) =>
		zs.base64(errorMsg),
	);
	zodSchema = extendSchemaWithMessage(zodSchema, jsonSchema, 'pattern', (zs, pattern, errorMsg) =>
		zs.regex(new RegExp(pattern), errorMsg),
	);
	zodSchema = extendSchemaWithMessage(
		zodSchema,
		jsonSchema,
		'minLength',
		(zs, minLength, errorMsg) => zs.min(minLength, errorMsg),
	);
	zodSchema = extendSchemaWithMessage(
		zodSchema,
		jsonSchema,
		'maxLength',
		(zs, maxLength, errorMsg) => zs.max(maxLength, errorMsg),
	);

	return zodSchema;
};
