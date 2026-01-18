"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Onfleet/WebhookMapping.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Onfleet 的Webhook节点。导入/依赖:外部:无；内部:无；本地:./interfaces。导出:webhookMapping。关键函数/方法:无。用于实现 n8n Webhook节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Onfleet/WebhookMapping.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Onfleet/WebhookMapping.py

import type { OnfleetWebhooksMapping } from './interfaces';

export const webhookMapping: OnfleetWebhooksMapping = {
	taskStarted: {
		name: 'Task Started',
		value: 'taskStarted',
		key: 0,
	},
	taskEta: {
		name: 'Task ETA',
		value: 'taskEta',
		key: 1,
	},
	taskArrival: {
		name: 'Task Arrival',
		value: 'taskArrival',
		key: 2,
	},
	taskCompleted: {
		name: 'Task Completed',
		value: 'taskCompleted',
		key: 3,
	},
	taskFailed: {
		name: 'Task Failed',
		value: 'taskFailed',
		key: 4,
	},
	workerDuty: {
		name: 'Worker Duty',
		value: 'workerDuty',
		key: 5,
	},
	taskCreated: {
		name: 'Task Created',
		value: 'taskCreated',
		key: 6,
	},
	taskUpdated: {
		name: 'Task Updated',
		value: 'taskUpdated',
		key: 7,
	},
	taskDeleted: {
		name: 'Task Deleted',
		value: 'taskDeleted',
		key: 8,
	},
	taskAssigned: {
		name: 'Task Assigned',
		value: 'taskAssigned',
		key: 9,
	},
	taskUnassigned: {
		name: 'Task Unassigned',
		value: 'taskUnassigned',
		key: 10,
	},
	taskDelayed: {
		name: 'Task Delayed',
		value: 'taskDelayed',
		key: 12,
	},
	taskCloned: {
		name: 'Task Cloned',
		value: 'taskCloned',
		key: 13,
	},
	smsRecipientResponseMissed: {
		name: 'SMS Recipient Response Missed',
		value: 'smsRecipientResponseMissed',
		key: 14,
	},
	workerCreated: {
		name: 'Worker Created',
		value: 'workerCreated',
		key: 15,
	},
	workerDeleted: {
		name: 'Worker Deleted',
		value: 'workerDeleted',
		key: 16,
	},
	SMSRecipientOptOut: {
		name: 'SMS Recipient Opt Out',
		value: 'SMSRecipientOptOut',
		key: 17,
	},
};
