"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/file/File.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./delete.operation、./get.operation、./getMany.operation、./load.operation 等1项。导出:deleteFile、get、getMany、upload、load、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/file/File.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/file/File_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as deleteFile from './delete.operation';
import * as get from './get.operation';
import * as getMany from './getMany.operation';
import * as load from './load.operation';
import * as upload from './upload.operation';

export { deleteFile, get, getMany, upload, load };

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
				name: 'Delete',
				value: 'deleteFile',
				description: 'Delete an uploaded file',
				action: 'Delete a file',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a details of an uploaded file',
				action: 'Get a file',
			},
			{
				name: 'Get Many',
				value: 'getMany',
				description: 'Get details of multiple uploaded files',
				action: 'Get many files',
			},
			{
				name: 'Load',
				value: 'load',
				description: 'Load a file into a session',
				action: 'Load a file',
			},
			{
				name: 'Upload',
				value: 'upload',
				description: 'Upload a file into a session',
				action: 'Upload a file',
			},
		],
		default: 'getMany',
	},
	...deleteFile.description,
	...get.description,
	...getMany.description,
	...load.description,
	...upload.description,
];
