"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Drive/v2/actions/drive/Drive.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Drive 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./deleteDrive.operation、./get.operation、./list.operation 等1项。导出:create、deleteDrive、get、list、update、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Drive/v2/actions/drive/Drive.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Drive/v2/actions/drive/Drive_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as deleteDrive from './deleteDrive.operation';
import * as get from './get.operation';
import * as list from './list.operation';
import * as update from './update.operation';

export { create, deleteDrive, get, list, update };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a shared drive',
				action: 'Create shared drive',
			},
			{
				name: 'Delete',
				value: 'deleteDrive',
				description: 'Permanently delete a shared drive',
				action: 'Delete shared drive',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a shared drive',
				action: 'Get shared drive',
			},
			{
				name: 'Get Many',
				value: 'list',
				description: 'Get the list of shared drives',
				action: 'Get many shared drives',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a shared drive',
				action: 'Update shared drive',
			},
		],
		default: 'create',
		displayOptions: {
			show: {
				resource: ['drive'],
			},
		},
	},
	...create.description,
	...deleteDrive.description,
	...get.description,
	...list.description,
	...update.description,
];
