"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/SyncroMsp.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/SyncroMspV1.node。导出:SyncroMsp。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/SyncroMsp.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/SyncroMsp_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { SyncroMspV1 } from './v1/SyncroMspV1.node';

export class SyncroMsp extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'SyncroMSP',
			name: 'syncroMsp',
			// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
			icon: 'file:syncromsp.png',
			group: ['output'],
			subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
			description: 'Manage contacts, tickets and more from Syncro MSP',
			defaultVersion: 1,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new SyncroMspV1(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
