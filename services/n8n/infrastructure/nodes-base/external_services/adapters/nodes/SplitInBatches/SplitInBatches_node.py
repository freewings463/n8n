"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SplitInBatches/SplitInBatches.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SplitInBatches 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/SplitInBatchesV1.node、./v2/SplitInBatchesV2.node、./v3/SplitInBatchesV3.node。导出:SplitInBatches。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SplitInBatches/SplitInBatches.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SplitInBatches/SplitInBatches_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { SplitInBatchesV1 } from './v1/SplitInBatchesV1.node';
import { SplitInBatchesV2 } from './v2/SplitInBatchesV2.node';
import { SplitInBatchesV3 } from './v3/SplitInBatchesV3.node';

export class SplitInBatches extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Split In Batches',
			name: 'splitInBatches',
			icon: 'fa:th-large',
			iconColor: 'dark-green',
			group: ['organization'],
			description: 'Split data into batches and iterate over each batch',
			defaultVersion: 3,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new SplitInBatchesV1(),
			2: new SplitInBatchesV2(),
			3: new SplitInBatchesV3(),
		};

		super(nodeVersions, baseDescription);
	}
}
