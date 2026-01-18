"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/employeeDocument/index.ts
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
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/employeeDocument/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/employeeDocument/__init__.py

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
				resource: ['employeeDocument'],
			},
		},
		options: [
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete an employee document',
				action: 'Delete an employee document',
			},
			{
				name: 'Download',
				value: 'download',
				description: 'Download an employee document',
				action: 'Download an employee document',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many employee documents',
				action: 'Get many employee documents',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update an employee document',
				action: 'Update an employee document',
			},
			{
				name: 'Upload',
				value: 'upload',
				description: 'Upload an employee document',
				action: 'Upload an employee document',
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
