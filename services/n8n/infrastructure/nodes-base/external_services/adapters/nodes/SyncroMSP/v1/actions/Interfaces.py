"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/actions/Interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:SyncroMsp、SyncroMspMapContact、SyncroMspMapCustomer、SyncroMspMapRmm、SyncroMspMapTicket、ContactProperties、CustomerProperties、RmmProperties 等2项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/actions/Interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/actions/Interfaces.py

import type { AllEntities, Entity, PropertiesOf } from 'n8n-workflow';

type SyncroMspMap = {
	contact: 'create' | 'delete' | 'get' | 'getAll' | 'update';
	customer: 'create' | 'delete' | 'get' | 'getAll' | 'update';
	rmm: 'create' | 'delete' | 'get' | 'getAll' | 'mute';
	ticket: 'create' | 'delete' | 'get' | 'getAll' | 'update';
};

export type SyncroMsp = AllEntities<SyncroMspMap>;

export type SyncroMspMapContact = Entity<SyncroMspMap, 'contact'>;
export type SyncroMspMapCustomer = Entity<SyncroMspMap, 'customer'>;
export type SyncroMspMapRmm = Entity<SyncroMspMap, 'rmm'>;
export type SyncroMspMapTicket = Entity<SyncroMspMap, 'ticket'>;

export type ContactProperties = PropertiesOf<SyncroMspMapContact>;
export type CustomerProperties = PropertiesOf<SyncroMspMapCustomer>;
export type RmmProperties = PropertiesOf<SyncroMspMapRmm>;
export type TicketProperties = PropertiesOf<SyncroMspMapTicket>;

export interface IAttachment {
	fields: {
		item?: object[];
	};
	actions: {
		item?: object[];
	};
}
