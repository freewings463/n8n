"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Salesforce/DocumentDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Salesforce 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:documentOperations、documentFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Salesforce/DocumentDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Salesforce/DocumentDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const documentOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['document'],
			},
		},
		options: [
			{
				name: 'Upload',
				value: 'upload',
				description: 'Upload a document',
				action: 'Upload a document',
			},
		],
		default: 'upload',
	},
];

export const documentFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                document:upload                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Title',
		name: 'title',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['document'],
				operation: ['upload'],
			},
		},
		description: 'Name of the file',
	},
	{
		displayName: 'Input Binary Field',
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		required: true,
		displayOptions: {
			show: {
				resource: ['document'],
				operation: ['upload'],
			},
		},
		placeholder: '',
		hint: 'The name of the input binary field containing the file to be uploaded',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['document'],
				operation: ['upload'],
			},
		},
		options: [
			{
				displayName: 'File Extension',
				name: 'fileExtension',
				type: 'string',
				default: '',
				placeholder: 'pdf',
				description:
					'File extension to use. If none is set, the value from the binary data will be used.',
			},
			{
				displayName: 'Link To Object ID',
				name: 'linkToObjectId',
				type: 'string',
				default: '',
				description: 'ID of the object you want to link this document to',
			},
			{
				displayName: 'Owner Name or ID',
				name: 'ownerId',
				type: 'options',
				typeOptions: {
					loadOptionsMethod: 'getUsers',
				},
				default: '',
				description:
					'ID of the owner of this document. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
			},
		],
	},
];
