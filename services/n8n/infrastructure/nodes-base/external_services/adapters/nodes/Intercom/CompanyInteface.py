"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Intercom/CompanyInteface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Intercom 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ICompany。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Intercom/CompanyInteface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Intercom/CompanyInteface.py

import type { IDataObject } from 'n8n-workflow';

export interface ICompany {
	remote_created_at?: string;
	company_id?: string;
	name?: string;
	monthly_spend?: number;
	plan?: string;
	size?: number;
	website?: string;
	industry?: string;
	custom_attributes?: IDataObject;
}
