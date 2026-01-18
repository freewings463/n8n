"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Onfleet/descriptions/HubDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Onfleet/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./DestinationDescription。导出:hubOperations、hubFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Onfleet/descriptions/HubDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Onfleet/descriptions/HubDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { destinationExternalField } from './DestinationDescription';

export const hubOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['hub'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new Onfleet hub',
				action: 'Create a hub',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many Onfleet hubs',
				action: 'Get many hubs',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update an Onfleet hub',
				action: 'Update a hub',
			},
		],
		default: 'getAll',
	},
];

const nameField = {
	displayName: 'Name',
	name: 'name',
	type: 'string',
	default: '',
	description: 'A name to identify the hub',
} as INodeProperties;

const teamsField = {
	displayName: 'Team Names or IDs',
	name: 'teams',
	type: 'multiOptions',
	typeOptions: {
		loadOptionsMethod: 'getTeams',
	},
	default: [],
	description:
		'These are the teams that this Hub will be assigned to. Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
} as INodeProperties;

export const hubFields: INodeProperties[] = [
	{
		displayName: 'Hub ID',
		name: 'id',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['hub'],
				operation: ['update'],
			},
		},
		default: '',
		required: true,
		description: 'The ID of the hub object for lookup',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['hub'],
				operation: ['getAll'],
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
				resource: ['hub'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 64,
		},
		default: 64,
		description: 'Max number of results to return',
	},
	{
		...nameField,
		displayOptions: {
			show: {
				resource: ['hub'],
				operation: ['create'],
			},
		},
		required: true,
	},
	{
		...destinationExternalField,
		displayOptions: {
			show: {
				resource: ['hub'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['hub'],
				operation: ['create'],
			},
		},
		options: [
			{
				...teamsField,
				required: false,
			},
		],
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['hub'],
				operation: ['update'],
			},
		},
		options: [
			{
				...destinationExternalField,
				required: false,
			},
			nameField,
			{
				...teamsField,
				required: false,
			},
		],
	},
];
