"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Merge/Merge.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Merge 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/MergeV1.node、./v2/MergeV2.node、./v3/MergeV3.node。导出:Merge。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Merge/Merge.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Merge/Merge_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { MergeV1 } from './v1/MergeV1.node';
import { MergeV2 } from './v2/MergeV2.node';
import { MergeV3 } from './v3/MergeV3.node';

export class Merge extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Merge',
			name: 'merge',
			icon: 'file:merge.svg',
			group: ['transform'],
			subtitle: '={{$parameter["mode"]}}',
			description: 'Merges data of multiple streams once data from both is available',
			defaultVersion: 3.2,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new MergeV1(baseDescription),
			2: new MergeV2(baseDescription),
			2.1: new MergeV2(baseDescription),
			3: new MergeV3(baseDescription),
			3.1: new MergeV3(baseDescription),
			3.2: new MergeV3(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
