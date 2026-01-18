"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/actions/rmm/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create、./del、./get、./getAll 等1项。导出:getAll、get、mute、del、create、descriptions。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/actions/rmm/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/actions/rmm/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create';
import * as del from './del';
import * as get from './get';
import * as getAll from './getAll';
import * as mute from './mute';

export { getAll, get, mute, del as delete, create };

export const descriptions = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['rmm'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create new RMM Alert',
				action: 'Create an RMM alert',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete RMM Alert',
				action: 'Delete an RMM alert',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve RMM Alert',
				action: 'Get an RMM alert',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve many RMM Alerts',
				action: 'Get many RMM alerts',
			},
			{
				name: 'Mute',
				value: 'mute',
				description: 'Mute RMM Alert',
				action: 'Mute an RMM alert',
			},
		],
		default: 'getAll',
	},
	...getAll.description,
	...get.description,
	...create.description,
	...del.description,
	...mute.description,
] as INodeProperties[];
