"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Grist/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Grist 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:GristCredentials、GristColumns、GristSortProperties、GristFilterProperties、GristGetAllOptions、GristDefinedFields、GristCreateRowPayload、GristUpdateRowPayload 等2项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Grist/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Grist/types.py

export type GristCredentials = {
	apiKey: string;
	planType: 'free' | 'paid' | 'selfHosted';
	customSubdomain?: string;
	selfHostedUrl?: string;
};

export type GristColumns = {
	columns: Array<{ id: string }>;
};

export type GristSortProperties = Array<{
	field: string;
	direction: 'asc' | 'desc';
}>;

export type GristFilterProperties = Array<{
	field: string;
	values: string;
}>;

export type GristGetAllOptions = {
	sort?: { sortProperties: GristSortProperties };
	filter?: { filterProperties: GristFilterProperties };
};

export type GristDefinedFields = Array<{
	fieldId: string;
	fieldValue: string;
}>;

export type GristCreateRowPayload = {
	records: Array<{
		fields: { [key: string]: any };
	}>;
};

export type GristUpdateRowPayload = {
	records: Array<{
		id: number;
		fields: { [key: string]: any };
	}>;
};

export type SendingOptions = 'defineInNode' | 'autoMapInputs';

export type FieldsToSend = { properties: GristDefinedFields };
