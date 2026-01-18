"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/file/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./deleteFile.operation、./list.operation、./upload.operation。导出:upload、deleteFile、list、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/file/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v2/actions/file/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as deleteFile from './deleteFile.operation';
import * as list from './list.operation';
import * as upload from './upload.operation';

export { upload, deleteFile, list };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Delete a File',
				value: 'deleteFile',
				action: 'Delete a file',
				description: 'Delete a file from the server',
			},
			{
				name: 'List Files',
				value: 'list',
				action: 'List files',
				description: "Returns a list of files that belong to the user's organization",
			},
			{
				name: 'Upload a File',
				value: 'upload',
				action: 'Upload a file',
				description: 'Upload a file that can be used across various endpoints',
			},
		],
		default: 'upload',
		displayOptions: {
			show: {
				resource: ['file'],
			},
		},
	},

	...upload.description,
	...deleteFile.description,
	...list.description,
];
