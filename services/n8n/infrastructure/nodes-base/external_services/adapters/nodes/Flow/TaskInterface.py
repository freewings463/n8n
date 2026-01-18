"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Flow/TaskInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Flow 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:ITask、TaskInfo。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Flow/TaskInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Flow/TaskInterface.py

export interface ITask {
	organization_id?: number;
	task?: TaskInfo;
}

export interface TaskInfo {
	workspace_id?: number;
	id?: number;
	name?: string;
	owner_id?: number;
	list_id?: number;
	starts_on?: string;
	due_on?: string;
	mirror_parent_subscribers?: boolean;
	mirror_parent_tags?: boolean;
	note_content?: string;
	note_mime_type?: string;
	parent_id?: number;
	position_list?: number;
	position_upcoming?: number;
	position?: number;
	section_id?: number;
	subscriptions?: number;
	tags?: string[];
	completed?: boolean;
}
