"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/alert/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./deleteAlert.operation、./executeResponder.operation、./get.operation 等5项。导出:create、executeResponder、deleteAlert、get、search、status、merge、promote 等2项。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/alert/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/alert/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as deleteAlert from './deleteAlert.operation';
import * as executeResponder from './executeResponder.operation';
import * as get from './get.operation';
import * as merge from './merge.operation';
import * as promote from './promote.operation';
import * as search from './search.operation';
import * as status from './status.operation';
import * as update from './update.operation';

export { create, executeResponder, deleteAlert, get, search, status, merge, promote, update };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		required: true,
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create an alert',
			},
			{
				name: 'Delete',
				value: 'deleteAlert',
				action: 'Delete an alert',
			},
			{
				name: 'Execute Responder',
				value: 'executeResponder',
				action: 'Execute responder on an alert',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get an alert',
			},
			{
				name: 'Merge Into Case',
				value: 'merge',
				action: 'Merge an alert into a case',
			},
			{
				name: 'Promote to Case',
				value: 'promote',
				action: 'Promote an alert to a case',
			},
			{
				name: 'Search',
				value: 'search',
				action: 'Search alerts',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update an alert',
			},
			{
				name: 'Update Status',
				value: 'status',
				action: 'Update an alert status',
			},
		],
		displayOptions: {
			show: {
				resource: ['alert'],
			},
		},
		default: 'create',
	},
	...create.description,
	...deleteAlert.description,
	...executeResponder.description,
	...get.description,
	...search.description,
	...status.description,
	...merge.description,
	...promote.description,
	...update.description,
];
