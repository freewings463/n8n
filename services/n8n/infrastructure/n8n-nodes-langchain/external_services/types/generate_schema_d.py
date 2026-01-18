"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/types/generate-schema.d.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/types 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:SchemaObject、SchemaArray、SchemaProperty、json。关键函数/方法:json。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/types/generate-schema.d.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/types/generate_schema_d.py

declare module 'generate-schema' {
	export interface SchemaObject {
		$schema: string;
		title?: string;
		type: string;
		properties?: {
			[key: string]: SchemaObject | SchemaArray | SchemaProperty;
		};
		required?: string[];
		items?: SchemaObject | SchemaArray;
	}

	export interface SchemaArray {
		type: string;
		items?: SchemaObject | SchemaArray | SchemaProperty;
		oneOf?: Array<SchemaObject | SchemaArray | SchemaProperty>;
		required?: string[];
	}

	export interface SchemaProperty {
		type: string | string[];
		format?: string;
	}

	export function json(title: string, schema: SchemaObject): SchemaObject;
	export function json(schema: SchemaObject): SchemaObject;
}
