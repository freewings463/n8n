"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Intercom/UserInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Intercom 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IUserCompany、IAvatar、IUser。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Intercom/UserInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Intercom/UserInterface.py

import type { IDataObject } from 'n8n-workflow';

export interface IUserCompany {
	company_id?: string;
}

export interface IAvatar {
	type?: string;
	image_url?: string;
}

export interface IUser {
	user_id?: string;
	id?: string;
	email?: string;
	phone?: string;
	name?: string;
	custom_attributes?: IDataObject;
	companies?: IUserCompany[];
	last_request_at?: number;
	signed_up_at?: string;
	unsubscribed_from_emails?: boolean;
	update_last_request_at?: boolean;
	last_seen_user_agent?: boolean;
	session_count?: number;
	avatar?: IAvatar;
	utm_source?: string;
	utm_medium?: string;
	utm_campaign?: string;
	utm_term?: string;
	utm_content?: string;
}
