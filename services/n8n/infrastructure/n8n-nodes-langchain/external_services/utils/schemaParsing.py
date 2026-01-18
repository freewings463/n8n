"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/schemaParsing.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils 的工具。导入/依赖:外部:generate-schema、json-schema、zod；内部:@n8n/json-schema-to-zod、n8n-workflow；本地:无。导出:generateSchemaFromExample、convertJsonSchemaToZod、throwIfToolSchema。关键函数/方法:makeAllPropertiesRequired、isPropertySchema、generateSchemaFromExample、throwIfToolSchema。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/schemaParsing.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/schemaParsing.py

import { jsonSchemaToZod } from '@n8n/json-schema-to-zod';
import { json as generateJsonSchema } from 'generate-schema';
import type { SchemaObject } from 'generate-schema';
import type { JSONSchema7 } from 'json-schema';
import type { IExecuteFunctions } from 'n8n-workflow';
import { NodeOperationError, jsonParse } from 'n8n-workflow';
import type { z } from 'zod';

function makeAllPropertiesRequired(schema: JSONSchema7): JSONSchema7 {
	function isPropertySchema(property: unknown): property is JSONSchema7 {
		return typeof property === 'object' && property !== null && 'type' in property;
	}

	// Handle object properties
	if (schema.type === 'object' && schema.properties) {
		const properties = Object.keys(schema.properties);
		if (properties.length > 0) {
			schema.required = properties;
		}

		for (const key of properties) {
			if (isPropertySchema(schema.properties[key])) {
				makeAllPropertiesRequired(schema.properties[key]);
			}
		}
	}

	// Handle arrays
	if (schema.type === 'array' && schema.items && isPropertySchema(schema.items)) {
		schema.items = makeAllPropertiesRequired(schema.items);
	}

	return schema;
}

export function generateSchemaFromExample(
	exampleJsonString: string,
	allFieldsRequired = false,
): JSONSchema7 {
	const parsedExample = jsonParse<SchemaObject>(exampleJsonString);

	const schema = generateJsonSchema(parsedExample) as JSONSchema7;

	if (allFieldsRequired) {
		return makeAllPropertiesRequired(schema);
	}

	return schema;
}

export function convertJsonSchemaToZod<T extends z.ZodTypeAny = z.ZodTypeAny>(schema: JSONSchema7) {
	return jsonSchemaToZod<T>(schema);
}

export function throwIfToolSchema(ctx: IExecuteFunctions, error: Error) {
	if (error?.message?.includes('tool input did not match expected schema')) {
		throw new NodeOperationError(
			ctx.getNode(),
			`${error.message}.
			This is most likely because some of your tools are configured to require a specific schema. This is not supported by Conversational Agent. Remove the schema from the tool configuration or use Tools agent instead.`,
		);
	}
}
