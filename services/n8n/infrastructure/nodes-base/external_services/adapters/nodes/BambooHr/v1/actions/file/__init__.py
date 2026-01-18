"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/file/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./del、./download、./getAll、./update 等1项。导出:del、download、getAll、update、upload、descriptions。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/file/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/file/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as del from './del';
import * as download from './download';
import * as getAll from './getAll';
import * as update from './update';
import * as upload from './upload';

export { del, download, getAll, update, upload };

export const descriptions: INodeProperties[] = [
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
				description: 'Delete a company file',
				action: 'Delete a file',
			},
			{
				name: 'Download',
				value: 'download',
				description: 'Download a company file',
				action: 'Download a file',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many company files',
				action: 'Get many files',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a company file',
				action: 'Update a file',
			},
			{
				name: 'Upload',
				value: 'upload',
				description: 'Upload a company file',
				action: 'Upload a file',
			},
		],
		default: 'delete',
	},
	...del.description,
	...download.description,
	...getAll.description,
	...update.description,
	...upload.description,
];
