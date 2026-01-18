"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Intercom/LeadInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Intercom 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ILeadCompany、IAvatar、ILead。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Intercom/LeadInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Intercom/LeadInterface.py

import type { IDataObject } from 'n8n-workflow';

export interface ILeadCompany {
	company_id?: string;
}

export interface IAvatar {
	type?: string;
	image_url?: string;
}

export interface ILead {
	user_id?: string;
	id?: string;
	email?: string;
	phone?: string;
	name?: string;
	custom_attributes?: IDataObject;
	companies?: ILeadCompany[];
	last_request_at?: number;
	unsubscribed_from_emails?: boolean;
	update_last_request_at?: boolean;
	avatar?: IAvatar;
	utm_source?: string;
	utm_medium?: string;
	utm_campaign?: string;
	utm_term?: string;
	utm_content?: string;
}
