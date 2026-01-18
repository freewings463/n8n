"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Jira/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Jira 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:JiraWebhook、JiraServerInfo。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Jira/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Jira/types.py

export type JiraWebhook = {
	id: number;
	name: string;
	createdDate: number;
	updatedDate: number;
	events: string[];
	configuration: {};
	url: string;
	active: boolean;
	scopeType: string;
	sslVerificationRequired: boolean;
	self?: string; // Only available for version < 10
};
export type JiraServerInfo = {
	baseUrl: string;
	version: string;
	versionNumbers: number[];
	deploymentType?: 'Cloud' | 'Server';
	buildNumber: number;
	buildDate: string;
	databaseBuildNumber: number;
	serverTime: string;
	scmInfo: string;
	serverTitle: string;
};
