"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/calendar/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./delete.operation、./get.operation、./getAll.operation 等1项。导出:create、del、get、getAll、update、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/calendar/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/actions/calendar/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as del from './delete.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';
import * as update from './update.operation';

export { create, del as delete, get, getAll, update };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['calendar'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new calendar',
				action: 'Create a calendar',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a calendar',
				action: 'Delete a calendar',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a calendar',
				action: 'Get a calendar',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'List and search calendars',
				action: 'Get many calendars',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a calendar',
				action: 'Update a calendar',
			},
		],
		default: 'getAll',
	},

	...create.description,
	...del.description,
	...get.description,
	...getAll.description,
	...update.description,
];
