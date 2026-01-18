"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Matrix/MediaDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Matrix 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:mediaOperations、mediaFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Matrix/MediaDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Matrix/MediaDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const mediaOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['media'],
			},
		},
		options: [
			{
				name: 'Upload',
				value: 'upload',
				description: 'Send media to a chat room',
				action: 'Upload media to a chatroom',
			},
		],
		default: 'upload',
	},
];

export const mediaFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                               media:upload                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Room Name or ID',
		name: 'roomId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getChannels',
		},
		default: '',
		displayOptions: {
			show: {
				resource: ['media'],
				operation: ['upload'],
			},
		},
		description:
			'Room ID to post. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		required: true,
	},
	{
		displayName: 'Input Binary Field',
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		required: true,
		hint: 'The name of the input binary field containing the file to be uploaded',
		displayOptions: {
			show: {
				resource: ['media'],
				operation: ['upload'],
			},
		},
	},
	{
		displayName: 'Media Type',
		name: 'mediaType',
		type: 'options',
		default: 'image',
		displayOptions: {
			show: {
				resource: ['media'],
				operation: ['upload'],
			},
		},
		options: [
			{
				name: 'File',
				value: 'file',
				description: 'General file',
			},
			{
				name: 'Image',
				value: 'image',
				description: 'Image media type',
			},
			{
				name: 'Audio',
				value: 'audio',
				description: 'Audio media type',
			},
			{
				name: 'Video',
				value: 'video',
				description: 'Video media type',
			},
		],
		description: 'Type of file being uploaded',
		placeholder: 'mxc://matrix.org/uploaded-media-uri',
		required: true,
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['media'],
				operation: ['upload'],
			},
		},
		options: [
			{
				displayName: 'File Name',
				name: 'fileName',
				type: 'string',
				default: '',
				description: 'Name of the file being uploaded',
			},
		],
	},
];
