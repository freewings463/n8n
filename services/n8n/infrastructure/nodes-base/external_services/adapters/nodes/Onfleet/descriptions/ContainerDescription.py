"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Onfleet/descriptions/ContainerDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Onfleet/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:containerOperations、containerFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Onfleet/descriptions/ContainerDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Onfleet/descriptions/ContainerDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const containerOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['container'],
			},
		},
		options: [
			{
				name: 'Add Tasks',
				value: 'addTask',
				description: 'Add task at index (or append)',
				action: 'Add tasks',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get container information',
				action: 'Get a container',
			},
			{
				name: 'Update Tasks',
				value: 'updateTask',
				description: "Fully replace a container's tasks",
				action: 'Update tasks',
			},
		],
		default: 'get',
	},
];

const containerTypeField = {
	displayName: 'Container Type',
	name: 'containerType',
	type: 'options',
	options: [
		{
			name: 'Organizations',
			value: 'organizations',
		},
		{
			name: 'Teams',
			value: 'teams',
		},
		{
			name: 'Workers',
			value: 'workers',
		},
	],
	default: '',
} as INodeProperties;

const containerIdField = {
	displayName: 'Container ID',
	name: 'containerId',
	type: 'string',
	default: '',
	description: 'The object ID according to the container chosen',
} as INodeProperties;

const insertTypeField = {
	displayName: 'Insert Type',
	name: 'type',
	type: 'options',
	options: [
		{
			name: 'Append',
			value: -1,
		},
		{
			name: 'Prepend',
			value: 0,
		},
		{
			name: 'At Specific Index',
			value: 1,
		},
	],
	default: '',
} as INodeProperties;

const indexField = {
	displayName: 'Index',
	name: 'index',
	type: 'number',
	default: 0,
	description: 'The index given indicates the position where the tasks are going to be inserted',
} as INodeProperties;

const tasksField = {
	displayName: 'Task IDs',
	name: 'tasks',
	type: 'string',
	typeOptions: {
		multipleValues: true,
		multipleValueButtonText: 'Add Task',
	},
	default: [],
	description: "Task's ID that are going to be used",
} as INodeProperties;

const considerDependenciesField = {
	displayName: 'Consider Dependencies',
	name: 'considerDependencies',
	type: 'boolean',
	default: false,
	description:
		"Whether to include the target task's dependency family (parent and child tasks) in the resulting assignment operation",
} as INodeProperties;

export const containerFields: INodeProperties[] = [
	{
		...containerTypeField,
		displayOptions: {
			show: {
				resource: ['container'],
				operation: ['get', 'addTask'],
			},
		},
		required: true,
	},
	{
		...containerIdField,
		displayOptions: {
			show: {
				resource: ['container'],
				operation: ['get', 'addTask', 'updateTask'],
			},
		},
		required: true,
	},
	{
		...insertTypeField,
		displayOptions: {
			show: {
				resource: ['container'],
				operation: ['addTask'],
			},
		},
		required: true,
	},
	{
		...indexField,
		displayOptions: {
			show: {
				resource: ['container'],
				operation: ['addTask'],
				type: [1],
			},
		},
		required: true,
	},
	{
		...tasksField,
		displayOptions: {
			show: {
				resource: ['container'],
				operation: ['addTask', 'updateTask'],
			},
		},
		required: true,
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		displayOptions: {
			show: {
				resource: ['container'],
				operation: ['addTask', 'updateTask'],
			},
		},
		options: [
			{
				...considerDependenciesField,
				required: false,
			},
		],
	},
];
