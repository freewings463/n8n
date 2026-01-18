"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/utils/its.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:../types。导出:its。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/utils/its.ts -> services/n8n/application/n8n-json-schema-to-zod/services/utils/its.py

import type { JsonSchema, JsonSchemaObject, Serializable } from '../types';

export const its = {
	an: {
		object: (x: JsonSchemaObject): x is JsonSchemaObject & { type: 'object' } =>
			x.type === 'object',
		array: (x: JsonSchemaObject): x is JsonSchemaObject & { type: 'array' } => x.type === 'array',
		anyOf: (
			x: JsonSchemaObject,
		): x is JsonSchemaObject & {
			anyOf: JsonSchema[];
		} => x.anyOf !== undefined,
		allOf: (
			x: JsonSchemaObject,
		): x is JsonSchemaObject & {
			allOf: JsonSchema[];
		} => x.allOf !== undefined,
		enum: (
			x: JsonSchemaObject,
		): x is JsonSchemaObject & {
			enum: Serializable | Serializable[];
		} => x.enum !== undefined,
	},
	a: {
		nullable: (x: JsonSchemaObject): x is JsonSchemaObject & { nullable: true } =>
			// eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unsafe-member-access
			(x as any).nullable === true,
		multipleType: (x: JsonSchemaObject): x is JsonSchemaObject & { type: string[] } =>
			Array.isArray(x.type),
		not: (
			x: JsonSchemaObject,
		): x is JsonSchemaObject & {
			not: JsonSchema;
		} => x.not !== undefined,
		const: (
			x: JsonSchemaObject,
		): x is JsonSchemaObject & {
			const: Serializable;
		} => x.const !== undefined,
		primitive: <T extends 'string' | 'number' | 'integer' | 'boolean' | 'null'>(
			x: JsonSchemaObject,
			p: T,
		): x is JsonSchemaObject & { type: T } => x.type === p,
		conditional: (
			x: JsonSchemaObject,
		): x is JsonSchemaObject & {
			if: JsonSchema;
			then: JsonSchema;
			else: JsonSchema;
		} => Boolean('if' in x && x.if && 'then' in x && 'else' in x && x.then && x.else),
		oneOf: (
			x: JsonSchemaObject,
		): x is JsonSchemaObject & {
			oneOf: JsonSchema[];
		} => x.oneOf !== undefined,
	},
};
