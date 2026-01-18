"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Baserow/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Baserow 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:BaserowCredentials、GetAllAdditionalOptions、LoadedResource、Accumulator、Row、FieldsUiValues、Operation。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Baserow/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Baserow/types.py

export type BaserowCredentials = {
	username: string;
	password: string;
	host: string;
};

export type GetAllAdditionalOptions = {
	order?: {
		fields: Array<{
			field: string;
			direction: string;
		}>;
	};
	filters?: {
		fields: Array<{
			field: string;
			operator: string;
			value: string;
		}>;
	};
	filterType: string;
	search: string;
};

export type LoadedResource = {
	id: number;
	name: string;
	type?: string;
};

export type Accumulator = {
	[key: string]: string;
};

export type Row = Record<string, string>;

export type FieldsUiValues = Array<{
	fieldId: string;
	fieldValue: string;
}>;

export type Operation = 'create' | 'delete' | 'update' | 'get' | 'getAll';
