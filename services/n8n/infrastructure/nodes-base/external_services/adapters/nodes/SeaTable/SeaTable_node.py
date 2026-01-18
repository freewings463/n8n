"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/SeaTable.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/SeaTableV1.node、./v2/SeaTableV2.node。导出:SeaTable。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/SeaTable.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/SeaTable_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { SeaTableV1 } from './v1/SeaTableV1.node';
import { SeaTableV2 } from './v2/SeaTableV2.node';

export class SeaTable extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'SeaTable',
			name: 'seaTable',
			icon: 'file:seaTable.svg',
			group: ['output'],
			subtitle: '={{$parameter["resource"] + ": " + $parameter["operation"]}}',
			description: 'Read, update, write and delete data from SeaTable',
			defaultVersion: 2,
			usableAsTool: true,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new SeaTableV1(baseDescription),
			2: new SeaTableV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
