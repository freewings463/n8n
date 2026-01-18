"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HighLevel/HighLevel.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HighLevel 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/HighLevelV1.node、./v2/HighLevelV2.node。导出:HighLevel。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HighLevel/HighLevel.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HighLevel/HighLevel_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { HighLevelV1 } from './v1/HighLevelV1.node';
import { HighLevelV2 } from './v2/HighLevelV2.node';

export class HighLevel extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'HighLevel',
			name: 'highLevel',
			icon: 'file:highLevel.svg',
			group: ['transform'],
			defaultVersion: 2,
			description: 'Consume HighLevel API',
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new HighLevelV1(baseDescription),
			2: new HighLevelV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
