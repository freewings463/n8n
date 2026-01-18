"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Twitter/V2/ListDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Twitter/V2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:listOperations、listFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Twitter/V2/ListDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Twitter/V2/ListDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const listOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['list'],
			},
		},
		options: [
			{
				name: 'Add Member',
				value: 'add',
				description: 'Add a member to a list',
				action: 'Add Member to List',
			},
		],
		default: 'add',
	},
];

export const listFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                list:add                        */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'List',
		name: 'list',
		type: 'resourceLocator',
		default: { mode: 'id', value: '' },
		required: true,
		description: 'The list you want to add the user to',
		displayOptions: {
			show: {
				operation: ['add'],
				resource: ['list'],
			},
		},
		modes: [
			{
				displayName: 'By ID',
				name: 'id',
				type: 'string',
				validation: [],
				placeholder: 'e.g. 99923132',
				url: '',
			},
			{
				displayName: 'By URL',
				name: 'url',
				type: 'string',
				validation: [],
				placeholder: 'e.g. https://twitter.com/i/lists/99923132',
				url: '',
			},
		],
	},
	{
		displayName: 'User',
		name: 'user',
		type: 'resourceLocator',
		default: { mode: 'username', value: '' },
		required: true,
		description: 'The user you want to add to the list',
		displayOptions: {
			show: {
				operation: ['add'],
				resource: ['list'],
			},
		},
		modes: [
			{
				displayName: 'By Username',
				name: 'username',
				type: 'string',
				validation: [],
				placeholder: 'e.g. n8n',
				url: '',
			},
			{
				displayName: 'By ID',
				name: 'id',
				type: 'string',
				validation: [],
				placeholder: 'e.g. 1068479892537384960',
				url: '',
			},
		],
	},
];
