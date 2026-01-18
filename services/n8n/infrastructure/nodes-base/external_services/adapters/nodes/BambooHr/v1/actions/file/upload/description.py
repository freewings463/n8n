"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/file/upload/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:fileUploadDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/file/upload/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/file/upload/description.py

import type { INodeProperties } from 'n8n-workflow';

export const fileUploadDescription: INodeProperties[] = [
	{
		displayName: 'Input Data Field Name',
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		displayOptions: {
			show: {
				operation: ['upload'],
				resource: ['file'],
			},
		},
		required: true,
		description:
			'The name of the input field containing the binary file data to be uploaded. Supported file types: PNG, JPEG.',
	},
	{
		displayName: 'Category Name or ID',
		name: 'categoryId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getCompanyFileCategories',
		},
		required: true,
		displayOptions: {
			show: {
				operation: ['upload'],
				resource: ['file'],
			},
		},
		default: '',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				operation: ['upload'],
				resource: ['file'],
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
