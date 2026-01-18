"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Salesforce/TaskInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Salesforce 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:ITask。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Salesforce/TaskInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Salesforce/TaskInterface.py

export interface ITask {
	TaskSubtype?: string;
	WhoId?: string;
	Status?: string;
	WhatId?: string;
	OwnerId?: string;
	Subject?: string;
	CallType?: string;
	Priority?: string;
	CallObject?: string;
	Description?: string;
	ActivityDate?: string;
	IsReminderSet?: boolean;
	RecurrenceType?: string;
	CallDisposition?: string;
	ReminderDateTime?: string;
	RecurrenceInstance?: string;
	RecurrenceInterval?: number;
	RecurrenceDayOfMonth?: number;
	CallDurationInSeconds?: number;
	RecurrenceEndDateOnly?: string;
	RecurrenceMonthOfYear?: string;
	RecurrenceDayOfWeekMask?: string;
	RecurrenceStartDateOnly?: string;
	RecurrenceTimeZoneSidKey?: string;
	RecurrenceRegeneratedType?: string;
}
