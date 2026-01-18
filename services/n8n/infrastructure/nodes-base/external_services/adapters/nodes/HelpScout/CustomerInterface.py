"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HelpScout/CustomerInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HelpScout 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ICustomer。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HelpScout/CustomerInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HelpScout/CustomerInterface.py

import type { IDataObject } from 'n8n-workflow';

export interface ICustomer {
	address?: IDataObject;
	age?: string;
	background?: string;
	chats?: IDataObject[];
	emails?: IDataObject[];
	firstName?: string;
	gender?: string;
	jobTitle?: string;
	lastName?: string;
	location?: string;
	organization?: string;
	phones?: IDataObject[];
	photoUrl?: string;
	properties?: IDataObject;
	socialProfiles?: IDataObject[];
	websites?: IDataObject[];
}
