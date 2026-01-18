"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Cockpit/FormDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Cockpit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:formOperations、formFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Cockpit/FormDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Cockpit/FormDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const formOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['form'],
			},
		},
		options: [
			{
				name: 'Submit a Form',
				value: 'submit',
				description: 'Store data from a form submission',
				action: 'Submit a form',
			},
		],
		default: 'submit',
	},
];

export const formFields: INodeProperties[] = [
	{
		displayName: 'Form',
		name: 'form',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['form'],
			},
		},
		default: '',
		required: true,
		description: 'Name of the form to operate on',
	},

	// Form:submit
	{
		displayName: 'JSON Data Fields',
		name: 'jsonDataFields',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				resource: ['form'],
				operation: ['submit'],
			},
		},
		description: 'Whether form fields should be set via the value-key pair UI or JSON',
	},
	{
		displayName: 'Form Data',
		name: 'dataFieldsJson',
		type: 'json',
		default: '',
		typeOptions: {
			alwaysOpenEditWindow: true,
		},
		displayOptions: {
			show: {
				jsonDataFields: [true],
				resource: ['form'],
				operation: ['submit'],
			},
		},
		description: 'Form data to send as JSON',
	},
	{
		displayName: 'Form Data',
		name: 'dataFieldsUi',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
		},
		default: {},
		displayOptions: {
			show: {
				jsonDataFields: [false],
				resource: ['form'],
				operation: ['submit'],
			},
		},
		options: [
			{
				displayName: 'Field',
				name: 'field',
				values: [
					{
						displayName: 'Name',
						name: 'name',
						type: 'string',
						default: '',
						description: 'Name of the field',
					},
					{
						displayName: 'Value',
						name: 'value',
						type: 'string',
						default: '',
						description: 'Value of the field',
					},
				],
			},
		],
		description: 'Form data to send',
	},
];
