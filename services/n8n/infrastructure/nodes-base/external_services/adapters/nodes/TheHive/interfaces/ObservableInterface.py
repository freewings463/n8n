"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHive/interfaces/ObservableInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHive/interfaces 的节点。导入/依赖:外部:无；内部:无；本地:./AlertInterface。导出:ObservableStatuses、ObservableStatus、ObservableDataTypes、ObservableDataType、IAttachment、IObservable。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHive/interfaces/ObservableInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHive/interfaces/ObservableInterface.py

import type { TLP } from './AlertInterface';

export const ObservableStatuses = {
	OK: 'Ok',
	DELETED: 'Deleted',
} as const;

export type ObservableStatus = (typeof ObservableStatuses)[keyof typeof ObservableStatuses];

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

export interface IAttachment {
	name?: string;
	size?: number;
	id?: string;
	contentType?: string;
	hashes: string[];
}
export interface IObservable {
	// Required attributes
	id?: string;
	data?: string;
	attachment?: IAttachment;
	dataType?: ObservableDataType;
	message?: string;
	startDate?: Date;
	tlp?: TLP;
	ioc?: boolean;
	status?: ObservableStatus;
	// Optional attributes
	tags: string[];
	// Backend generated attributes

	createdBy?: string;
	createdAt?: Date;
	updatedBy?: string;
	upadtedAt?: Date;
}
