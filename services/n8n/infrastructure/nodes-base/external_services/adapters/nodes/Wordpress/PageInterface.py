"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Wordpress/PageInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Wordpress 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IPage。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Wordpress/PageInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Wordpress/PageInterface.py

export interface IPage {
	author?: number;
	comment_status?: string;
	content?: string;
	featured_media?: number;
	id?: number;
	menu_order?: number;
	page?: number;
	parent?: number;
	password?: string;
	ping_status?: string;
	slug?: string;
	status?: string;
	template?: string;
	title?: string;
}
