"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Lemlist/v1/descriptions/UnsubscribeDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Lemlist/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:unsubscribeOperations、unsubscribeFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Lemlist/v1/descriptions/UnsubscribeDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Lemlist/v1/descriptions/UnsubscribeDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const unsubscribeOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'add',
		options: [
			{
				name: 'Add',
				value: 'add',
				action: 'Add an email to an unsubscribe list',
			},
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete an email from an unsubscribe list',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many unsubscribed emails',
			},
		],
		displayOptions: {
			show: {
				resource: ['unsubscribe'],
			},
		},
	},
];

export const unsubscribeFields: INodeProperties[] = [
	// ----------------------------------
	//        unsubscribe: add
	// ----------------------------------
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		default: '',
		description: 'Email to add to the unsubscribes',
		displayOptions: {
			show: {
				resource: ['unsubscribe'],
				operation: ['add'],
			},
		},
	},

	// ----------------------------------
	//        unsubscribe: delete
	// ----------------------------------
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		default: '',
		description: 'Email to delete from the unsubscribes',
		displayOptions: {
			show: {
				resource: ['unsubscribe'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------
	//       unsubscribe: getAll
	// ----------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['unsubscribe'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 5,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
			maxValue: 1000,
		},
		displayOptions: {
			show: {
				resource: ['unsubscribe'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
];
