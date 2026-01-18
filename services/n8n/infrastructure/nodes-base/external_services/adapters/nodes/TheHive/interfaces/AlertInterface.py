"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHive/interfaces/AlertInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHive/interfaces 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:AlertStatuses、AlertStatus、TLPs、TLP、IAlert。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHive/interfaces/AlertInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHive/interfaces/AlertInterface.py

import type { IDataObject } from 'n8n-workflow';

export const AlertStatuses = {
	NEW: 'New',
	UPDATED: 'Updated',
	IGNORED: 'Ignored',
	IMPORTED: 'Imported',
} as const;

export type AlertStatus = (typeof AlertStatuses)[keyof typeof AlertStatuses];

export const TLPs = {
	white: 0,
	green: 1,
	amber: 2,
	red: 3,
} as const;

export type TLP = (typeof TLPs)[keyof typeof TLPs];

export interface IAlert {
	// Required attributes
	id?: string;
	title?: string;
	description?: string;
	severity?: number;
	date?: Date;
	tags?: string[];
	tlp?: TLP;
	status?: AlertStatus;
	type?: string;
	source?: string;
	sourceRef?: string;
	artifacts?: IDataObject[];
	follow?: boolean;

	// Optional attributes
	caseTemplate?: string;

	// Backend generated attributes
	lastSyncDate?: Date;
	case?: string;

	createdBy?: string;
	createdAt?: Date;
	updatedBy?: string;
	upadtedAt?: Date;
}
