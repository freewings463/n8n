"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/S3/V2/FolderDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/S3 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:folderOperations、folderFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/S3/V2/FolderDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/S3/V2/FolderDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const folderOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['folder'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a folder',
				action: 'Create a folder',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a folder',
				action: 'Delete a folder',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many folders',
				action: 'Get many folders',
			},
		],
		default: 'create',
	},
];

export const folderFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                folder:create                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Bucket Name',
		name: 'bucketName',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['folder'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Folder Name',
		name: 'folderName',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['folder'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		displayOptions: {
			show: {
				resource: ['folder'],
				operation: ['create'],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Parent Folder Key',
				name: 'parentFolderKey',
				type: 'string',
				default: '',
				description: 'Parent folder you want to create the folder in',
			},
			{
				displayName: 'Requester Pays',
				name: 'requesterPays',
				type: 'boolean',
				default: false,
				description:
					'Whether the requester will pay for requests and data transfer. While Requester Pays is enabled, anonymous access to this bucket is disabled.',
			},
			{
				displayName: 'Storage Class',
				name: 'storageClass',
				type: 'options',
				options: [
					{
						name: 'Deep Archive',
						value: 'deepArchive',
					},
					{
						name: 'Glacier',
						value: 'glacier',
					},
					{
						name: 'Intelligent Tiering',
						value: 'intelligentTiering',
					},
					{
						name: 'One Zone IA',
						value: 'onezoneIA',
					},
					{
						name: 'Reduced Redundancy',
						value: 'RecudedRedundancy',
					},
					{
						name: 'Standard',
						value: 'standard',
					},
					{
						name: 'Standard IA',
						value: 'standardIA',
					},
				],
				default: 'standard',
				description: 'Amazon S3 storage classes',
			},
		],
	},
	/* -------------------------------------------------------------------------- */
	/*                                folder:delete                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Bucket Name',
		name: 'bucketName',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['folder'],
				operation: ['delete'],
			},
		},
	},
	{
		displayName: 'Folder Key',
		name: 'folderKey',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['folder'],
				operation: ['delete'],
			},
		},
	},
	/* -------------------------------------------------------------------------- */
	/*                                 folder:getAll                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Bucket Name',
		name: 'bucketName',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['folder'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['folder'],
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
				operation: ['getAll'],
				resource: ['folder'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 500,
		},
		default: 100,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['folder'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Fetch Owner',
				name: 'fetchOwner',
				type: 'boolean',
				default: false,
				// eslint-disable-next-line n8n-nodes-base/node-param-description-boolean-without-whether
				description:
					'The owner field is not present in listV2 by default, if you want to return owner field with each key in the result then set the fetch owner field to true',
			},
			{
				displayName: 'Folder Key',
				name: 'folderKey',
				type: 'string',
				default: '',
			},
		],
	},
];
