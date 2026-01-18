"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Transform/RemoveDuplicates/RemoveDuplicates.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Transform/RemoveDuplicates 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/RemoveDuplicatesV1.node、./v2/RemoveDuplicatesV2.node。导出:RemoveDuplicates。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Transform/RemoveDuplicates/RemoveDuplicates.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Transform/RemoveDuplicates/RemoveDuplicates_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { RemoveDuplicatesV1 } from './v1/RemoveDuplicatesV1.node';
import { RemoveDuplicatesV2 } from './v2/RemoveDuplicatesV2.node';
export class RemoveDuplicates extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Remove Duplicates',
			name: 'removeDuplicates',
			icon: 'file:removeDuplicates.svg',
			group: ['transform'],
			defaultVersion: 2,
			description: 'Delete items with matching field values',
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new RemoveDuplicatesV1(baseDescription),
			1.1: new RemoveDuplicatesV1(baseDescription),
			2: new RemoveDuplicatesV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
