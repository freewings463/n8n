"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHive/descriptions/EventsDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHive/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:eventsDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHive/descriptions/EventsDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHive/descriptions/EventsDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const eventsDescription: INodeProperties[] = [
	{
		displayName: 'Events',
		name: 'events',
		type: 'multiOptions',
		default: [],
		required: true,
		description: 'Events types',
		displayOptions: {
			show: {
				'@version': [1],
			},
		},
		options: [
			{
				name: '*',
				value: '*',
				description: 'Any time any event is triggered (Wildcard Event)',
			},
			{
				name: 'Alert Created',
				value: 'alert_create',
				description: 'Triggered when an alert is created',
			},
			{
				name: 'Alert Deleted',
				value: 'alert_delete',
				description: 'Triggered when an alert is deleted',
			},
			{
				name: 'Alert Updated',
				value: 'alert_update',
				description: 'Triggered when an alert is updated',
			},
			{
				name: 'Case Created',
				value: 'case_create',
				description: 'Triggered when a case is created',
			},
			{
				name: 'Case Deleted',
				value: 'case_delete',
				description: 'Triggered when a case is deleted',
			},
			{
				name: 'Case Updated',
				value: 'case_update',
				description: 'Triggered when a case is updated',
			},
			{
				name: 'Log Created',
				value: 'case_task_log_create',
				description: 'Triggered when a task log is created',
			},
			{
				name: 'Log Deleted',
				value: 'case_task_log_delete',
				description: 'Triggered when a task log is deleted',
			},
			{
				name: 'Log Updated',
				value: 'case_task_log_update',
				description: 'Triggered when a task log is updated',
			},
			{
				name: 'Observable Created',
				value: 'case_artifact_create',
				description: 'Triggered when an observable is created',
			},
			{
				name: 'Observable Deleted',
				value: 'case_artifact_delete',
				description: 'Triggered when an observable is deleted',
			},
			{
				name: 'Observable Updated',
				value: 'case_artifact_update',
				description: 'Triggered when an observable is updated',
			},
			{
				name: 'Task Created',
				value: 'case_task_create',
				description: 'Triggered when a task is created',
			},
			{
				name: 'Task Deleted',
				value: 'case_task_delete',
				description: 'Triggered when a task is deleted',
			},
			{
				name: 'Task Updated',
				value: 'case_task_update',
				description: 'Triggered when a task is updated',
			},
		],
	},
	{
		displayName: 'Events',
		name: 'events',
		type: 'multiOptions',
		default: [],
		required: true,
		description: 'Events types',
		displayOptions: {
			show: {
				'@version': [2],
			},
		},
		options: [
			{
				name: '*',
				value: '*',
				description: 'Any time any event is triggered (Wildcard Event)',
			},
			{
				name: 'Alert Created',
				value: 'alert_create',
				description: 'Triggered when an alert is created',
			},
			{
				name: 'Alert Deleted',
				value: 'alert_delete',
				description: 'Triggered when an alert is deleted',
			},
			{
				name: 'Alert Updated',
				value: 'alert_update',
				description: 'Triggered when an alert is updated',
			},
			{
				name: 'Case Created',
				value: 'case_create',
				description: 'Triggered when a case is created',
			},
			{
				name: 'Case Deleted',
				value: 'case_delete',
				description: 'Triggered when a case is deleted',
			},
			{
				name: 'Case Updated',
				value: 'case_update',
				description: 'Triggered when a case is updated',
			},
			{
				name: 'Log Created',
				value: 'case_task_log_create',
				description: 'Triggered when a task log is created',
			},
			{
				name: 'Log Deleted',
				value: 'case_task_log_delete',
				description: 'Triggered when a task log is deleted',
			},
			{
				name: 'Log Updated',
				value: 'case_task_log_update',
				description: 'Triggered when a task log is updated',
			},
			{
				name: 'Observable Created',
				value: 'case_artifact_create',
				description: 'Triggered when an observable is created',
			},
			{
				name: 'Observable Deleted',
				value: 'case_artifact_delete',
				description: 'Triggered when an observable is deleted',
			},
			{
				name: 'Observable Updated',
				value: 'case_artifact_update',
				description: 'Triggered when an observable is updated',
			},
			{
				name: 'Task Created',
				value: 'case_task_create',
				description: 'Triggered when a task is created',
			},
			{
				name: 'Task Updated',
				value: 'case_task_update',
				description: 'Triggered when a task is updated',
			},
		],
	},
];
