"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Cortex/AnalyzerInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Cortex 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:JobStatuses、JobStatus、TLPs、TLP、ObservableDataTypes、ObservableDataType、IJob、IAnalyzer 等1项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Cortex/AnalyzerInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Cortex/AnalyzerInterface.py

import type { IDataObject } from 'n8n-workflow';

export const JobStatuses = {
	WAITING: 'Waiting',
	INPROGRESS: 'InProgress',
	SUCCESS: 'Success',
	FAILURE: 'Failure',
	DELETED: 'Deleted',
} as const;

export type JobStatus = (typeof JobStatuses)[keyof typeof JobStatuses];

export const TLPs = {
	white: 0,
	green: 1,
	amber: 2,
	red: 3,
} as const;

export type TLP = (typeof TLPs)[keyof typeof TLPs];

export const ObservableDataTypes = {
	domain: 'domain',
	file: 'file',
	filename: 'filename',
	fqdn: 'fqdn',
	hash: 'hash',
	ip: 'ip',
	mail: 'mail',
	mail_subject: 'mail_subject',
	other: 'other',
	regexp: 'regexp',
	registry: 'registry',
	uri_path: 'uri_path',
	url: 'url',
	'user-agent': 'user-agent',
} as const;

export type ObservableDataType = (typeof ObservableDataTypes)[keyof typeof ObservableDataTypes];

export interface IJob {
	id?: string;
	organization?: string;
	analyzerDefinitionId?: string;
	analyzerId?: string;
	analyzerName?: string;
	dataType?: ObservableDataType;
	status?: JobStatus;
	data?: string;
	attachment?: IDataObject;
	parameters?: IDataObject;
	message?: string;
	tlp?: TLP;
	startDate?: Date;
	endDate?: Date;
	createdAt?: Date;
	createdBy?: string;
	updatedAt?: Date;
	updatedBy?: Date;
	report?: IDataObject | string;
}
export interface IAnalyzer {
	id?: string;
	analyzerDefinitionId?: string;
	name?: string;
	version?: string;
	description?: string;
	author?: string;
	url?: string;
	license?: string;
	dataTypeList?: ObservableDataType[];
	baseConfig?: string;
	jobCache?: number;
	rate?: number;
	rateUnit?: string;
	configuration?: IDataObject;
	createdBy?: string;
	updatedAt?: Date;
	updatedBy?: Date;
}

export interface IResponder {
	id?: string;
	name?: string;
	version?: string;
	description?: string;
	dataTypeList?: string[];
	maxTlp?: number;
	maxPap?: number;
	cortexIds?: string[] | undefined;
}
