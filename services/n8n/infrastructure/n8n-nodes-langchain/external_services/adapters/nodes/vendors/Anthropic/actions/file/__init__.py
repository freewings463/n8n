"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/actions/file/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Anthropic 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./delete.operation、./get.operation、./list.operation、./upload.operation。导出:deleteFile、get、list、upload、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/actions/file/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Anthropic/actions/file/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as deleteFile from './delete.operation';
import * as get from './get.operation';
import * as list from './list.operation';
import * as upload from './upload.operation';

export { deleteFile, get, list, upload };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Upload File',
				value: 'upload',
				action: 'Upload a file',
				description: 'Upload a file to the Anthropic API for later use',
			},
			{
				name: 'Get File Metadata',
				value: 'get',
				action: 'Get file metadata',
				description: 'Get metadata for a file from the Anthropic API',
			},
			{
				name: 'List Files',
				value: 'list',
				action: 'List files',
				description: 'List files from the Anthropic API',
			},
			{
				name: 'Delete File',
				value: 'deleteFile',
				action: 'Delete a file',
				description: 'Delete a file from the Anthropic API',
			},
		],
		default: 'upload',
		displayOptions: {
			show: {
				resource: ['file'],
			},
		},
	},
	...deleteFile.description,
	...get.description,
	...list.description,
	...upload.description,
];
