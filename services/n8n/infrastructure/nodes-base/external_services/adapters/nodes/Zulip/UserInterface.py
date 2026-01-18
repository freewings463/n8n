"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Zulip/UserInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Zulip 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IUser。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Zulip/UserInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Zulip/UserInterface.py

import type { IDataObject } from 'n8n-workflow';

export interface IUser {
	client_gravatar?: boolean;
	include_custom_profile_fields?: boolean;
	full_name?: string;
	is_admin?: boolean;
	is_guest?: boolean;
	profile_data?: [IDataObject];
	email?: string;
	password?: string;
	short_name?: string;
	role?: number;
}
