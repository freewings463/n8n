"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/observable/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./deleteObservable.operation、./executeAnalyzer.operation、./executeResponder.operation 等3项。导出:create、deleteObservable、executeAnalyzer、executeResponder、get、search、update、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/observable/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/observable/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as deleteObservable from './deleteObservable.operation';
import * as executeAnalyzer from './executeAnalyzer.operation';
import * as executeResponder from './executeResponder.operation';
import * as get from './get.operation';
import * as search from './search.operation';
import * as update from './update.operation';

export { create, deleteObservable, executeAnalyzer, executeResponder, get, search, update };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		required: true,
		default: 'create',
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create an observable',
			},
			{
				name: 'Delete',
				value: 'deleteObservable',
				action: 'Delete an observable',
			},
			{
				name: 'Execute Analyzer',
				value: 'executeAnalyzer',
				action: 'Execute analyzer on an observable',
			},
			{
				name: 'Execute Responder',
				value: 'executeResponder',
				action: 'Execute responder on an observable',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get an observable',
			},
			{
				name: 'Search',
				value: 'search',
				action: 'Search observables',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update an observable',
			},
		],
		displayOptions: {
			show: {
				resource: ['observable'],
			},
		},
	},
	...create.description,
	...deleteObservable.description,
	...executeAnalyzer.description,
	...executeResponder.description,
	...get.description,
	...search.description,
	...update.description,
];
