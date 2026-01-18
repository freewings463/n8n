"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Drive/v2/actions/file/File.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Drive 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./copy.operation、./createFromText.operation、./deleteFile.operation、./download.operation 等4项。导出:copy、createFromText、deleteFile、download、move、share、update、upload 等1项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Drive/v2/actions/file/File.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Drive/v2/actions/file/File_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as copy from './copy.operation';
import * as createFromText from './createFromText.operation';
import * as deleteFile from './deleteFile.operation';
import * as download from './download.operation';
import * as move from './move.operation';
import * as share from './share.operation';
import * as update from './update.operation';
import * as upload from './upload.operation';

export { copy, createFromText, deleteFile, download, move, share, update, upload };

export const description: INodeProperties[] = [
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
				name: 'Copy',
				value: 'copy',
				description: 'Create a copy of an existing file',
				action: 'Copy file',
			},
			{
				name: 'Create From Text',
				value: 'createFromText',
				description: 'Create a file from a provided text',
				action: 'Create file from text',
			},
			{
				name: 'Delete',
				value: 'deleteFile',
				description: 'Permanently delete a file',
				action: 'Delete a file',
			},
			{
				name: 'Download',
				value: 'download',
				description: 'Download a file',
				action: 'Download file',
			},
			{
				name: 'Move',
				value: 'move',
				description: 'Move a file to another folder',
				action: 'Move file',
			},
			{
				name: 'Share',
				value: 'share',
				description: 'Add sharing permissions to a file',
				action: 'Share file',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a file',
				action: 'Update file',
			},
			{
				name: 'Upload',
				value: 'upload',
				description: 'Upload an existing file to Google Drive',
				action: 'Upload file',
			},
		],
		default: 'upload',
	},
	...copy.description,
	...deleteFile.description,
	...createFromText.description,
	...download.description,
	...move.description,
	...share.description,
	...update.description,
	...upload.description,
];
