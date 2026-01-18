"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/chains/InformationExtractor/helpers.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/chains/InformationExtractor 的工具。导入/依赖:外部:zod；内部:无；本地:./types。导出:makeZodSchemaFromAttributes。关键函数/方法:makeAttributeSchema、makeZodSchemaFromAttributes。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/chains/InformationExtractor/helpers.ts -> services/n8n/tests/n8n-nodes-langchain/unit/nodes/chains/InformationExtractor/helpers.py

import { z } from 'zod';

import type { AttributeDefinition } from './types';

function makeAttributeSchema(attributeDefinition: AttributeDefinition, required: boolean = true) {
	let schema: z.ZodTypeAny;

	if (attributeDefinition.type === 'string') {
		schema = z.string();
	} else if (attributeDefinition.type === 'number') {
		schema = z.number();
	} else if (attributeDefinition.type === 'boolean') {
		schema = z.boolean();
	} else if (attributeDefinition.type === 'date') {
		schema = z.string().date();
	} else {
		schema = z.unknown();
	}

	if (!required) {
		schema = schema.optional();
	}

	return schema.describe(attributeDefinition.description);
}

export function makeZodSchemaFromAttributes(attributes: AttributeDefinition[]) {
	const schemaEntries = attributes.map((attr) => [
		attr.name,
		makeAttributeSchema(attr, attr.required),
	]);

	return z.object(Object.fromEntries(schemaEntries));
}
