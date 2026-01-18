"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/employeeDocument/upload/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的节点。导入/依赖:外部:无；内部:无；本地:../../Interfaces。导出:employeeDocumentUploadDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/employeeDocument/upload/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/employeeDocument/upload/description.py

import type { EmployeeDocumentProperties } from '../../Interfaces';

export const employeeDocumentUploadDescription: EmployeeDocumentProperties = [
	{
		displayName: 'Employee ID',
		name: 'employeeId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['upload'],
				resource: ['employeeDocument'],
			},
		},
		default: '',
		description: 'ID of the employee',
	},
	{
		displayName: 'Employee Document Category ID',
		name: 'categoryId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['upload'],
				resource: ['employeeDocument'],
			},
		},
		default: '',
	},
	{
		displayName: 'Input Data Field Name',
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		displayOptions: {
			show: {
				operation: ['upload'],
				resource: ['employeeDocument'],
			},
		},
		required: true,
		description:
			'The name of the input field containing the binary file data to be uploaded. Supported file types: PNG, JPEG.',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['upload'],
				resource: ['employeeDocument'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Share with Employee',
				name: 'share',
				type: 'boolean',
				default: true,
				description: 'Whether this file is shared or not',
			},
		],
	},
];
