"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/employee/create/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的节点。导入/依赖:外部:无；内部:无；本地:./shareDescription、../../Interfaces。导出:employeeCreateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/employee/create/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/employee/create/description.py

import { createEmployeeSharedDescription } from './shareDescription';
import type { EmployeeProperties } from '../../Interfaces';

export const employeeCreateDescription: EmployeeProperties = [
	{
		displayName: 'Synced with Trax Payroll',
		name: 'synced',
		type: 'boolean',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['employee'],
			},
		},
		default: false,
		description:
			'Whether the employee to create was added to a pay schedule synced with Trax Payroll',
	},
	{
		displayName: 'First Name',
		name: 'firstName',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['employee'],
			},
		},
		default: '',
	},
	{
		displayName: 'Last Name',
		name: 'lastName',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['employee'],
			},
		},
		default: '',
	},
	...(createEmployeeSharedDescription(true) as EmployeeProperties),
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['employee'],
			},
		},
		options: [
			...createEmployeeSharedDescription(false),
			{
				displayName: 'Work Email',
				name: 'workEmail',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Work Phone',
				name: 'workPhone',
				type: 'string',
				default: '',
			},
		],
	},
];
