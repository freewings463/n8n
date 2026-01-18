"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Jira/IssueInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Jira 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IFields、IIssue、INotify、INotificationRecipients、NotificationRecipientsRestrictions。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Jira/IssueInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Jira/IssueInterface.py

import type { IDataObject } from 'n8n-workflow';

export interface IFields {
	assignee?: IDataObject;
	description?: string;
	issuetype?: IDataObject;
	labels?: string[];
	parent?: IDataObject;
	priority?: IDataObject;
	project?: IDataObject;
	summary?: string;
	reporter?: IDataObject;
	components?: IDataObject[];
}

export interface IIssue {
	fields?: IFields;
	transition?: IDataObject;
}

export interface INotify {
	subject?: string;
	textBody?: string;
	htmlBody?: string;
	to?: INotificationRecipients;
	restrict?: NotificationRecipientsRestrictions;
}

export interface INotificationRecipients {
	reporter?: boolean;
	assignee?: boolean;
	watchers?: boolean;
	voters?: boolean;
	users?: IDataObject[];
	groups?: IDataObject[];
}

export interface NotificationRecipientsRestrictions {
	groups?: IDataObject[];
}
