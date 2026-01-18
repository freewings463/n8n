"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Grafana/descriptions/TeamMemberDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Grafana/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:teamMemberOperations、teamMemberFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Grafana/descriptions/TeamMemberDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Grafana/descriptions/TeamMemberDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const teamMemberOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['teamMember'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add a member to a team',
				action: 'Add a team member',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many team members',
				action: 'Get many team members',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove a member from a team',
				action: 'Remove a team member',
			},
		],
		default: 'add',
	},
];

export const teamMemberFields: INodeProperties[] = [
	// ----------------------------------------
	//            teamMember: add
	// ----------------------------------------
	{
		displayName: 'User Name or ID',
		name: 'userId',
		description:
			'User to add to a team. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		type: 'options',
		required: true,
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getUsers',
		},
		displayOptions: {
			show: {
				resource: ['teamMember'],
				operation: ['add'],
			},
		},
	},
	{
		displayName: 'Team Name or ID',
		name: 'teamId',
		description:
			'Team to add the user to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		type: 'options',
		required: true,
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getTeams',
		},
		displayOptions: {
			show: {
				resource: ['teamMember'],
				operation: ['add'],
			},
		},
	},

	// ----------------------------------------
	//            teamMember: remove
	// ----------------------------------------
	{
		displayName: 'User Name or ID',
		name: 'memberId',
		description:
			'User to remove from the team. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		type: 'options',
		required: true,
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getUsers',
		},
		displayOptions: {
			show: {
				resource: ['teamMember'],
				operation: ['remove'],
			},
		},
	},
	{
		displayName: 'Team Name or ID',
		name: 'teamId',
		description:
			'Team to remove the user from. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		type: 'options',
		required: true,
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getTeams',
		},
		displayOptions: {
			show: {
				resource: ['teamMember'],
				operation: ['remove'],
			},
		},
	},

	// ----------------------------------------
	//            teamMember: getAll
	// ----------------------------------------
	{
		displayName: 'Team Name or ID',
		name: 'teamId',
		description:
			'Team to retrieve all members from. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		typeOptions: {
			loadOptionsMethod: 'getTeams',
		},
		type: 'options',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['teamMember'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['teamMember'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 50,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
		},
		displayOptions: {
			show: {
				resource: ['teamMember'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
];
