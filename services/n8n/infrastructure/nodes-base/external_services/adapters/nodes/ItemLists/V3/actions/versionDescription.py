"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ItemLists/V3/actions/versionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ItemLists/V3 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./itemList。导出:versionDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ItemLists/V3/actions/versionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ItemLists/V3/actions/versionDescription.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import { NodeConnectionTypes, type INodeTypeDescription } from 'n8n-workflow';

import * as itemList from './itemList';

export const versionDescription: INodeTypeDescription = {
	displayName: 'Item Lists',
	name: 'itemLists',
	icon: 'file:itemLists.svg',
	group: ['input'],
	subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
	description: 'Helper for working with lists of items and transforming arrays',
	version: [3, 3.1],
	defaults: {
		name: 'Item Lists',
	},
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	credentials: [],
	properties: [
		{
			displayName: 'Resource',
			name: 'resource',
			type: 'hidden',
			options: [
				{
					name: 'Item List',
					value: 'itemList',
				},
			],
			default: 'itemList',
		},
		...itemList.description,
	],
};
