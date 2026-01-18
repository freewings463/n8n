"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/src/types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod/src 的类型。导入/依赖:外部:zod；内部:无；本地:无。导出:Serializable、JsonSchema、JsonSchemaObject、ParserSelector、ParserOverride、JsonSchemaToZodOptions、Refs。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/src/types.ts -> services/n8n/application/n8n-json-schema-to-zod/services/types.py

import type { ZodTypeAny } from 'zod';

export type Serializable =
	| { [key: string]: Serializable }
	| Serializable[]
	| string
	| number
	| boolean
	| null;

export type JsonSchema = JsonSchemaObject | boolean;
export type JsonSchemaObject = {
	// left permissive by design
	type?: string | string[];

	// object
	properties?: { [key: string]: JsonSchema };
	additionalProperties?: JsonSchema;
	unevaluatedProperties?: JsonSchema;
	patternProperties?: { [key: string]: JsonSchema };
	minProperties?: number;
	maxProperties?: number;
	required?: string[] | boolean;
	propertyNames?: JsonSchema;

	// array
	items?: JsonSchema | JsonSchema[];
	additionalItems?: JsonSchema;
	minItems?: number;
	maxItems?: number;
	uniqueItems?: boolean;

	// string
	minLength?: number;
	maxLength?: number;
	pattern?: string;
	format?: string;

	// number
	minimum?: number;
	maximum?: number;
	exclusiveMinimum?: number | boolean;
	exclusiveMaximum?: number | boolean;
	multipleOf?: number;

	// unions
	anyOf?: JsonSchema[];
	allOf?: JsonSchema[];
	oneOf?: JsonSchema[];

	if?: JsonSchema;
	then?: JsonSchema;
	else?: JsonSchema;

	// shared
	const?: Serializable;
	enum?: Serializable[];

	errorMessage?: { [key: string]: string | undefined };

	description?: string;
	default?: Serializable;
	readOnly?: boolean;
	not?: JsonSchema;
	contentEncoding?: string;
	nullable?: boolean;
};

export type ParserSelector = (schema: JsonSchemaObject, refs: Refs) => ZodTypeAny;
export type ParserOverride = (schema: JsonSchemaObject, refs: Refs) => ZodTypeAny | undefined;

export type JsonSchemaToZodOptions = {
	withoutDefaults?: boolean;
	withoutDescribes?: boolean;
	parserOverride?: ParserOverride;
	depth?: number;
};

export type Refs = JsonSchemaToZodOptions & {
	path: Array<string | number>;
	seen: Map<object | boolean, { n: number; r: ZodTypeAny | undefined }>;
};
