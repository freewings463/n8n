"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/QuickBase/FileDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/QuickBase 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:fileOperations、fileFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/QuickBase/FileDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/QuickBase/FileDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const fileOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['file'],
			},
		},
		options: [
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a file',
				action: 'Delete a file',
			},
			{
				name: 'Download',
				value: 'download',
				description: 'Download a file',
				action: 'Download a file',
			},
		],
		default: 'download',
	},
];

export const fileFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                file:download                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Table ID',
		name: 'tableId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['download', 'delete'],
			},
		},
		description: 'The table identifier',
	},
	{
		displayName: 'Record ID',
		name: 'recordId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['download', 'delete'],
			},
		},
		description: 'The unique identifier of the record',
	},
	{
		displayName: 'Field ID',
		name: 'fieldId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['download', 'delete'],
			},
		},
		description: 'The unique identifier of the field',
	},
	{
		displayName: 'Version Number',
		name: 'versionNumber',
		type: 'number',
		default: 1,
		required: true,
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['download', 'delete'],
			},
		},
		description: 'The file attachment version number',
	},
	{
		displayName: 'Input Binary Field',
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['download'],
			},
		},
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		hint: 'The name of the input binary field containing the file to be written',
		required: true,
	},
];
