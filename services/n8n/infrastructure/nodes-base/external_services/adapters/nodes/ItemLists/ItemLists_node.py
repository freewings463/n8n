"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ItemLists/ItemLists.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ItemLists 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./V1/ItemListsV1.node、./V2/ItemListsV2.node、./V3/ItemListsV3.node。导出:ItemLists。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ItemLists/ItemLists.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ItemLists/ItemLists_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { ItemListsV1 } from './V1/ItemListsV1.node';
import { ItemListsV2 } from './V2/ItemListsV2.node';
import { ItemListsV3 } from './V3/ItemListsV3.node';

export class ItemLists extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Item Lists',
			name: 'itemLists',
			icon: 'file:itemLists.svg',
			group: ['input'],
			hidden: true,
			subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
			description: 'Helper for working with lists of items and transforming arrays',
			defaultVersion: 3.1,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new ItemListsV1(baseDescription),
			2: new ItemListsV2(baseDescription),
			2.1: new ItemListsV2(baseDescription),
			2.2: new ItemListsV2(baseDescription),
			3: new ItemListsV3(baseDescription),
			3.1: new ItemListsV3(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
