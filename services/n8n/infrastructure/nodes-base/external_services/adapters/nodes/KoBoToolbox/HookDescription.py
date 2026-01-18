"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/KoBoToolbox/HookDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/KoBoToolbox 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:hookOperations、hookFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/KoBoToolbox/HookDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/KoBoToolbox/HookDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const hookOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['hook'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a single hook definition',
				action: 'Get a hook',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'List many hooks on a form',
				action: 'Get Many hooks',
			},
			{
				name: 'Logs',
				value: 'getLogs',
				description: 'Get hook logs',
				action: 'Get Logs for a hook',
			},
			{
				name: 'Retry All',
				value: 'retryAll',
				description: 'Retry all failed attempts for a given hook',
				action: 'Retry All hooks',
			},
			{
				name: 'Retry One',
				value: 'retryOne',
				description: 'Retry a specific hook',
				action: 'Retry One hook',
			},
		],
		default: 'getAll',
	},
];

export const hookFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                hook:get                                    */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Form Name or ID',
		name: 'formId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'loadForms',
		},
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['hook'],
				operation: ['get', 'retryOne', 'retryAll', 'getLogs', 'getAll'],
			},
		},
		description:
			'Form ID (e.g. aSAvYreNzVEkrWg5Gdcvg). Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Hook ID',
		name: 'hookId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['hook'],
				operation: ['get', 'retryOne', 'retryAll', 'getLogs'],
			},
		},
		default: '',
		description: 'Hook ID (starts with h, e.g. hVehywQ2oXPYGHJHKtqth4)',
	},
	/* -------------------------------------------------------------------------- */
	/*                                hook:getAll                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Hook Log ID',
		name: 'logId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['hook'],
				operation: ['retryOne'],
			},
		},
		default: '',
		description: 'Hook log ID (starts with hl, e.g. hlSbGKaUKzTVNoWEVMYbLHe)',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		required: true,
		default: false,
		displayOptions: {
			show: {
				resource: ['hook'],
				operation: ['getAll'],
			},
		},
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		typeOptions: {
			maxValue: 3000,
		},
		displayOptions: {
			show: {
				resource: ['hook'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
		default: 1000,
		description: 'Max number of results to return',
	},
	/* -------------------------------------------------------------------------- */
	/*                                hook:getLogs                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Log Status',
		name: 'status',
		type: 'options',
		displayOptions: {
			show: {
				resource: ['hook'],
				operation: ['getLogs'],
			},
		},
		default: '',
		description: 'Only retrieve logs with a specific status',
		options: [
			{
				name: 'All',
				value: '',
			},
			{
				name: 'Failed',
				value: '0',
			},
			{
				name: 'Pending',
				value: '1',
			},
			{
				name: 'Success',
				value: '2',
			},
		],
	},
	{
		displayName: 'Start Date',
		name: 'startDate',
		type: 'dateTime',
		displayOptions: {
			show: {
				resource: ['hook'],
				operation: ['getLogs'],
			},
		},
		default: '',
		description: 'Minimum date for the hook log to retrieve',
	},
	{
		displayName: 'End Date',
		name: 'endDate',
		type: 'dateTime',
		displayOptions: {
			show: {
				resource: ['hook'],
				operation: ['getLogs'],
			},
		},
		default: '',
		description: 'Maximum date for the hook log to retrieve',
	},
];
