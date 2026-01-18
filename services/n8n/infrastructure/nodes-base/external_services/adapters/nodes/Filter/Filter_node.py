"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Filter/Filter.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Filter 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./V1/FilterV1.node、./V2/FilterV2.node。导出:Filter。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Filter/Filter.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Filter/Filter_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { FilterV1 } from './V1/FilterV1.node';
import { FilterV2 } from './V2/FilterV2.node';

export class Filter extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Filter',
			name: 'filter',
			icon: 'fa:filter',
			iconColor: 'light-blue',
			group: ['transform'],
			description: 'Remove items matching a condition',
			defaultVersion: 2.3,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new FilterV1(baseDescription),
			2: new FilterV2(baseDescription),
			2.1: new FilterV2(baseDescription),
			2.2: new FilterV2(baseDescription),
			2.3: new FilterV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
