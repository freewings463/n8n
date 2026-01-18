"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/employee/update/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的节点。导入/依赖:外部:无；内部:无；本地:./sharedDescription、../../Interfaces。导出:employeeUpdateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/employee/update/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/employee/update/description.py

import { updateEmployeeSharedDescription } from './sharedDescription';
import type { EmployeeProperties } from '../../Interfaces';

export const employeeUpdateDescription: EmployeeProperties = [
	{
		displayName: 'Employee ID',
		name: 'employeeId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['employee'],
			},
		},
		default: '',
	},
	{
		displayName: 'Synced with Trax Payroll',
		name: 'synced',
		type: 'boolean',
		required: true,
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['employee'],
			},
		},
		default: false,
		description:
			'Whether the employee to create was added to a pay schedule synced with Trax Payroll',
	},
	...(updateEmployeeSharedDescription(true) as EmployeeProperties),
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['employee'],
			},
		},
		options: [
			...updateEmployeeSharedDescription(false),
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
