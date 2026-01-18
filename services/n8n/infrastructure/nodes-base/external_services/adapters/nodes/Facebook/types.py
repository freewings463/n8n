"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Facebook/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Facebook 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:FacebookEvent、FacebookPageEventEntry、FacebookWebhookSubscription。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Facebook/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Facebook/types.py

export interface FacebookEvent {
	object: string;
	entry: FacebookPageEventEntry[];
}

export interface FacebookPageEventEntry {
	id: string;
	time: number;
	changes: [
		{
			field: 'leadgen';
			value: {
				ad_id: string;
				form_id: string;
				leadgen_id: string;
				created_time: number;
				page_id: string;
				adgroup_id: string;
			};
		},
	];
}

export interface FacebookWebhookSubscription {
	object: string;
	callback_url: string;
	fields: string[];
	status: boolean;
}
