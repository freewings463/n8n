"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/FreshworksCrm/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/FreshworksCrm 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:FreshworksCrmApiCredentials、FreshworksConfigResponse、LoadedResource、LoadOption、LoadedCurrency、LoadedUser、SalesAccounts、ViewsResponse 等1项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/FreshworksCrm/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/FreshworksCrm/types.py

export type FreshworksCrmApiCredentials = {
	apiKey: string;
	domain: string;
};

export type FreshworksConfigResponse<T> = {
	[key: string]: T[];
};

export type LoadedResource = {
	id: string;
	name: string;
};

export type LoadOption = {
	name: string;
	value: string;
};

export type LoadedCurrency = {
	currency_code: string;
	id: string;
};

export type LoadedUser = {
	id: string;
	display_name: string;
};

export type SalesAccounts = {
	sales_accounts?: number[];
};

export type ViewsResponse = {
	filters: View[];
	meta: object;
};

export type View = {
	id: number;
	name: string;
	model_class_name: string;
	user_id: number;
	is_default: boolean;
	updated_at: string;
	user_name: string;
	current_user_permissions: string[];
};
