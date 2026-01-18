"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/versionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./asset、./base、./link、./row。导出:versionDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/versionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/versionDescription.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import { NodeConnectionTypes, type INodeTypeDescription } from 'n8n-workflow';

import * as asset from './asset';
import * as base from './base';
import * as link from './link';
import * as row from './row';

export const versionDescription: INodeTypeDescription = {
	displayName: 'SeaTable',
	name: 'seaTable',
	icon: 'file:seaTable.svg',
	group: ['output'],
	version: 2,
	subtitle: '={{$parameter["resource"] + ": " + $parameter["operation"]}}',
	description: 'Consume the SeaTable API',
	defaults: {
		name: 'SeaTable',
	},
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	credentials: [
		{
			name: 'seaTableApi',
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
					name: 'Row',
					value: 'row',
				},
				{
					name: 'Base',
					value: 'base',
				},
				{
					name: 'Link',
					value: 'link',
				},
				{
					name: 'Asset',
					value: 'asset',
				},
			],
			default: 'row',
		},
		...row.descriptions,
		...base.descriptions,
		...link.descriptions,
		...asset.descriptions,
	],
};
