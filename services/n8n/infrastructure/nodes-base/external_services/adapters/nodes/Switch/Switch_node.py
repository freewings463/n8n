"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Switch/Switch.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Switch 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./V1/SwitchV1.node、./V2/SwitchV2.node、./V3/SwitchV3.node。导出:Switch。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Switch/Switch.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Switch/Switch_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { SwitchV1 } from './V1/SwitchV1.node';
import { SwitchV2 } from './V2/SwitchV2.node';
import { SwitchV3 } from './V3/SwitchV3.node';

export class Switch extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Switch',
			name: 'switch',
			icon: 'fa:map-signs',
			iconColor: 'light-blue',
			group: ['transform'],
			description: 'Route items depending on defined expression or rules',
			defaultVersion: 3.4,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new SwitchV1(baseDescription),
			2: new SwitchV2(baseDescription),
			3: new SwitchV3(baseDescription),
			3.1: new SwitchV3(baseDescription),
			3.2: new SwitchV3(baseDescription),
			3.3: new SwitchV3(baseDescription),
			3.4: new SwitchV3(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
