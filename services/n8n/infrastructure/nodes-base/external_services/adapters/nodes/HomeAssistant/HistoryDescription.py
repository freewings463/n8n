"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HomeAssistant/HistoryDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HomeAssistant 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:historyOperations、historyFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HomeAssistant/HistoryDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HomeAssistant/HistoryDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const historyOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['history'],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many state changes',
				action: 'Get many state changes',
			},
		],
		default: 'getAll',
	},
];

export const historyFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                history:getLogbookEntries                   */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['history'],
			},
		},
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['history'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		default: 50,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['history'],
				operation: ['getAll'],
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
				displayName: 'Entity IDs',
				name: 'entityIds',
				type: 'string',
				default: '',
				description: 'The entities IDs separated by comma',
			},
			{
				displayName: 'Minimal Response',
				name: 'minimalResponse',
				type: 'boolean',
				default: false,
				description: 'Whether to only return <code>last_changed</code> and state for states',
			},
			{
				displayName: 'Significant Changes Only',
				name: 'significantChangesOnly',
				type: 'boolean',
				default: false,
				description: 'Whether to only return significant state changes',
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
