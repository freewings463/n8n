"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/node.description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./alert、./case、./comment、./log 等4项。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/node.description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/node_description.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import { NodeConnectionTypes, type INodeTypeDescription } from 'n8n-workflow';

import * as alert from './alert';
import * as case_ from './case';
import * as comment from './comment';
import * as log from './log';
import * as observable from './observable';
import * as page from './page';
import * as query from './query';
import * as task from './task';

export const description: INodeTypeDescription = {
	displayName: 'TheHive 5',
	name: 'theHiveProject',
	icon: 'file:thehiveproject.svg',
	group: ['transform'],
	subtitle: '={{$parameter["operation"]}} : {{$parameter["resource"]}}',
	version: 1,
	description: 'Consume TheHive 5 API',
	defaults: {
		name: 'TheHive 5',
	},
	usableAsTool: true,
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	credentials: [
		{
			name: 'theHiveProjectApi',
			required: true,
		},
	],
	properties: [
		{
			displayName: 'Resource',
			name: 'resource',
			type: 'options',
			noDataExpression: true,
			required: true,
			options: [
				{
					name: 'Alert',
					value: 'alert',
				},
				{
					name: 'Case',
					value: 'case',
				},
				{
					name: 'Comment',
					value: 'comment',
				},
				{
					name: 'Observable',
					value: 'observable',
				},
				{
					name: 'Page',
					value: 'page',
				},
				{
					name: 'Query',
					value: 'query',
				},
				{
					name: 'Task',
					value: 'task',
				},
				{
					name: 'Task Log',
					value: 'log',
				},
			],
			default: 'alert',
		},

		...alert.description,
		...case_.description,
		...comment.description,
		...log.description,
		...observable.description,
		...page.description,
		...query.description,
		...task.description,
	],
};
