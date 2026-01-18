"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HomeAssistant/LogDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HomeAssistant 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:logOperations、logFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HomeAssistant/LogDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HomeAssistant/LogDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const logOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['log'],
			},
		},
		options: [
			{
				name: 'Get Error Logs',
				value: 'getErroLogs',
				description: 'Get a log for a specific entity',
				action: 'Get a log for an entity',
			},
			{
				name: 'Get Logbook Entries',
				value: 'getLogbookEntries',
				description: 'Get all logs',
				action: 'Get all logs for an entity',
			},
		],
		default: 'getErroLogs',
	},
];

export const logFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                log:getLogbookEntries                       */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['log'],
				operation: ['getLogbookEntries'],
			},
		},
		options: [
			{
				displayName: 'End Time',
				name: 'endTime',
				type: 'dateTime',
				default: '',
				description: 'The end of the period',
			},
			{
				displayName: 'Entity ID',
				name: 'entityId',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Start Time',
				name: 'startTime',
				type: 'dateTime',
				default: '',
				description: 'The beginning of the period',
			},
		],
	},
];
