"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Grafana/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Grafana 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:GrafanaCredentials、DashboardUpdatePayload、DashboardUpdateFields、LoadedDashboards、LoadedFolders、LoadedTeams、LoadedUsers。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Grafana/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Grafana/types.py

export type GrafanaCredentials = {
	apiKey: string;
	baseUrl: string;
};

export type DashboardUpdatePayload = {
	overwrite: true;
	dashboard: {
		uid: string;
		title?: string;
	};
};

export type DashboardUpdateFields = {
	title?: string;
	folderId?: string;
};

export type LoadedDashboards = Array<{
	id: number;
	title: string;
}>;

export type LoadedFolders = LoadedDashboards;

export type LoadedTeams = {
	teams: Array<{
		id: number;
		name: string;
	}>;
};

export type LoadedUsers = Array<{
	userId: number;
	email: string;
}>;
