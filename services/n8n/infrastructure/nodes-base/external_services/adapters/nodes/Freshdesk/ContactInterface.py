"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Freshdesk/ContactInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Freshdesk 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ICreateContactBody。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Freshdesk/ContactInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Freshdesk/ContactInterface.py

import type { IDataObject } from 'n8n-workflow';

export interface ICreateContactBody {
	address?: string;
	// avatar?: object;
	company_id?: number;
	custom_fields?: IDataObject;
	description?: string;
	email?: string;
	job_title?: string;
	language?: string;
	mobile?: string;
	name?: string;
	other_companies?: string[];
	other_emails?: string[];
	phone?: string;
	tags?: string[];
	time_zone?: string;
	twitter_id?: string;
	unique_external_id?: string;
	view_all_tickets?: boolean;
}
