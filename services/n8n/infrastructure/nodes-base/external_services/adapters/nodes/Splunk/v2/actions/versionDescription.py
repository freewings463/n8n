"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v2/actions/versionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./alert、./report、./search、./user。导出:versionDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v2/actions/versionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v2/actions/versionDescription.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import { NodeConnectionTypes, type INodeTypeDescription } from 'n8n-workflow';

import * as alert from './alert';
import * as report from './report';
import * as search from './search';
import * as user from './user';

export const versionDescription: INodeTypeDescription = {
	displayName: 'Splunk',
	name: 'splunk',
	icon: 'file:splunk.svg',
	group: ['transform'],
	version: 2,
	subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
	description: 'Consume the Splunk Enterprise API',
	defaults: {
		name: 'Splunk',
	},
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	credentials: [
		{
			name: 'splunkApi',
			required: true,
		},
	],
	properties: [
		{
			displayName: 'Resource',
			name: 'resource',
			type: 'options',
			noDataExpression: true,
			options: [
				{
					name: 'Alert',
					value: 'alert',
				},
				{
					name: 'Report',
					value: 'report',
				},
				{
					name: 'Search',
					value: 'search',
				},
				{
					name: 'User',
					value: 'user',
				},
			],
			default: 'search',
		},

		...alert.description,
		...report.description,
		...search.description,
		...user.description,
	],
};
