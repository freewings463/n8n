"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Set/Set.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Set 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/SetV1.node、./v2/SetV2.node。导出:Set。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Set/Set.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Set/Set_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { SetV1 } from './v1/SetV1.node';
import { SetV2 } from './v2/SetV2.node';

export class Set extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Set',
			name: 'set',
			icon: 'fa:pen',
			group: ['input'],
			description: 'Add or edit fields on an input item and optionally remove other fields',
			defaultVersion: 3.4,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new SetV1(baseDescription),
			2: new SetV1(baseDescription),
			3: new SetV2(baseDescription),
			3.1: new SetV2(baseDescription),
			3.2: new SetV2(baseDescription),
			3.3: new SetV2(baseDescription),
			3.4: new SetV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
