"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Matrix/RoomMemberDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Matrix 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:roomMemberOperations、roomMemberFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Matrix/RoomMemberDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Matrix/RoomMemberDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const roomMemberOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['roomMember'],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many members',
				action: 'Get many room members',
			},
		],
		default: 'getAll',
	},
];

export const roomMemberFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                             roomMember:getAll                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Room Name or ID',
		name: 'roomId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getChannels',
		},
		displayOptions: {
			show: {
				resource: ['roomMember'],
				operation: ['getAll'],
			},
		},
		default: '',
		required: true,
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		displayOptions: {
			show: {
				resource: ['roomMember'],
				operation: ['getAll'],
			},
		},
		default: {},
		description: 'Filtering options',
		placeholder: 'Add filter',
		options: [
			{
				displayName: 'Exclude Membership',
				name: 'notMembership',
				type: 'options',
				default: '',
				description:
					'Excludes members whose membership is other than selected (uses OR filter with membership)',
				options: [
					{
						name: 'Any',
						value: '',
						description: 'Any user membership',
					},
					{
						name: 'Ban',
						value: 'ban',
						description: 'Users removed from the room',
					},
					{
						name: 'Invite',
						value: 'invite',
						description: 'Users invited to join',
					},
					{
						name: 'Join',
						value: 'join',
						description: 'Users currently in the room',
					},
					{
						name: 'Leave',
						value: 'leave',
						description: 'Users who left',
					},
				],
			},
			{
				displayName: 'Membership',
				name: 'membership',
				type: 'options',
				default: '',
				description:
					'Only fetch users with selected membership status (uses OR filter with exclude membership)',
				options: [
					{
						name: 'Any',
						value: '',
						description: 'Any user membership',
					},
					{
						name: 'Ban',
						value: 'ban',
						description: 'Users removed from the room',
					},
					{
						name: 'Invite',
						value: 'invite',
						description: 'Users invited to join',
					},
					{
						name: 'Join',
						value: 'join',
						description: 'Users currently in the room',
					},
					{
						name: 'Leave',
						value: 'leave',
						description: 'Users who left',
					},
				],
			},
		],
	},
];
