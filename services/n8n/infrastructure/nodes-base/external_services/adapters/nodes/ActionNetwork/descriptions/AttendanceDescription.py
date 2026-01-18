"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActionNetwork/descriptions/AttendanceDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActionNetwork/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./SharedFields。导出:attendanceOperations、attendanceFields。关键函数/方法:makeSimpleField。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActionNetwork/descriptions/AttendanceDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActionNetwork/descriptions/AttendanceDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { makeSimpleField } from './SharedFields';

export const attendanceOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['attendance'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create an attendance',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get an attendance',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many attendances',
			},
		],
		default: 'create',
	},
];

export const attendanceFields: INodeProperties[] = [
	// ----------------------------------------
	//            attendance: create
	// ----------------------------------------
	{
		displayName: 'Person ID',
		name: 'personId',
		description: 'ID of the person to create an attendance for',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['attendance'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Event ID',
		name: 'eventId',
		description: 'ID of the event to create an attendance for',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['attendance'],
				operation: ['create'],
			},
		},
	},
	makeSimpleField('attendance', 'create'),

	// ----------------------------------------
	//             attendance: get
	// ----------------------------------------
	{
		displayName: 'Event ID',
		name: 'eventId',
		description: 'ID of the event whose attendance to retrieve',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['attendance'],
				operation: ['get'],
			},
		},
	},
	{
		displayName: 'Attendance ID',
		name: 'attendanceId',
		description: 'ID of the attendance to retrieve',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['attendance'],
				operation: ['get'],
			},
		},
	},
	makeSimpleField('attendance', 'get'),

	// ----------------------------------------
	//            attendance: getAll
	// ----------------------------------------
	{
		displayName: 'Event ID',
		name: 'eventId',
		description: 'ID of the event to create an attendance for',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['attendance'],
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
				resource: ['attendance'],
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
				resource: ['attendance'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	makeSimpleField('attendance', 'getAll'),
];
