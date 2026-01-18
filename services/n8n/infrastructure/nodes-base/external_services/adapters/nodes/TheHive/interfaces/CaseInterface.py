"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHive/interfaces/CaseInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHive/interfaces 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./AlertInterface。导出:ICase、CaseStatuses、CaseStatus、CaseResolutionStatuses、CaseResolutionStatus、CaseImpactStatuses、CaseImpactStatus。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHive/interfaces/CaseInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHive/interfaces/CaseInterface.py

import type { IDataObject } from 'n8n-workflow';

import type { TLP } from './AlertInterface';
export interface ICase {
	// Required attributes
	id?: string;
	title?: string;
	description?: string;
	severity?: number;
	startDate?: Date;
	owner?: string;
	flag?: boolean;
	tlp?: TLP;
	tags?: string[];

	// Optional attributes
	resolutionStatus?: CaseResolutionStatus;
	impactStatus?: CaseImpactStatus;
	summary?: string;
	endDate?: Date;
	metrics?: IDataObject;

	// Backend generated attributes
	status?: CaseStatus;
	caseId?: number; // auto-generated attribute
	mergeInto?: string;
	mergeFrom?: string[];

	createdBy?: string;
	createdAt?: Date;
	updatedBy?: string;
	upadtedAt?: Date;
}

export const CaseStatuses = {
	OPEN: 'Open',
	RESOLVED: 'Resolved',
	DELETED: 'Deleted',
} as const;

export type CaseStatus = (typeof CaseStatuses)[keyof typeof CaseStatuses];

export const CaseResolutionStatuses = {
	INDETERMINATE: 'Indeterminate',
	FALSEPOSITIVE: 'FalsePositive',
	TRUEPOSITIVE: 'TruePositive',
	OTHER: 'Other',
	DUPLICATED: 'Duplicated',
} as const;

export type CaseResolutionStatus =
	(typeof CaseResolutionStatuses)[keyof typeof CaseResolutionStatuses];

export const CaseImpactStatuses = {
	NOIMPACT: 'NoImpact',
	WITHIMPACT: 'WithImpact',
	NOTAPPLICABLE: 'NotApplicable',
} as const;

export type CaseImpactStatus = (typeof CaseImpactStatuses)[keyof typeof CaseImpactStatuses];
