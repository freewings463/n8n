"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/KoBoToolbox/FileDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/KoBoToolbox 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:fileOperations、fileFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/KoBoToolbox/FileDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/KoBoToolbox/FileDescription.py

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
				name: 'Create',
				value: 'create',
				description: 'Create a file',
				action: 'Create a file',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete file',
				action: 'Delete a file',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a file content',
				action: 'Get a file content',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many files',
				action: 'Get many files',
			},
		],
		default: 'get',
	},
];

export const fileFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                file:*                                    */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Form Name or ID',
		name: 'formId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'loadForms',
		},
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['file'],
			},
		},
		description:
			'Form ID (e.g. aSAvYreNzVEkrWg5Gdcvg). Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	/* -------------------------------------------------------------------------- */
	/*                                file:delete                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'File ID',
		name: 'fileId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['delete', 'get'],
			},
		},
		description: 'Uid of the file (should start with "af" e.g. "afQoJxA4kmKEXVpkH6SYbhb"',
	},
	{
		displayName: 'Property Name',
		name: 'binaryPropertyName',
		type: 'string',
		required: true,
		default: 'data',
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['get'],
			},
		},
		description: 'Name of the binary property to write the file into',
	},
	{
		displayName: 'Download File Content',
		name: 'download',
		type: 'boolean',
		required: true,
		default: false,
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['get'],
			},
		},
		description: 'Whether to download the file content into a binary property',
	},
	{
		displayName: 'File Upload Mode',
		name: 'fileMode',
		type: 'options',
		required: true,
		default: 'binary',
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['create'],
			},
		},
		options: [
			{
				name: 'Binary File',
				value: 'binary',
			},
			{
				name: 'URL',
				value: 'url',
			},
		],
	},
	{
		displayName: 'Property Name',
		name: 'binaryPropertyName',
		type: 'string',
		required: true,
		default: 'data',
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['create'],
				fileMode: ['binary'],
			},
		},
		description:
			'Name of the binary property containing the file to upload. Supported types: image, audio, video, csv, xml, zip.',
	},
	{
		displayName: 'File URL',
		name: 'fileUrl',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['create'],
				fileMode: ['url'],
			},
		},
		description: 'HTTP(s) link to the file to upload',
	},
];
