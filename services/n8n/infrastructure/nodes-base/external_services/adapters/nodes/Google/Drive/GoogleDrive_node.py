"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Drive/GoogleDrive.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Drive 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/GoogleDriveV1.node、./v2/GoogleDriveV2.node。导出:GoogleDrive。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Drive/GoogleDrive.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Drive/GoogleDrive_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { GoogleDriveV1 } from './v1/GoogleDriveV1.node';
import { GoogleDriveV2 } from './v2/GoogleDriveV2.node';

export class GoogleDrive extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Google Drive',
			name: 'googleDrive',
			icon: 'file:googleDrive.svg',
			group: ['input'],
			subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
			description: 'Access data on Google Drive',
			defaultVersion: 3,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new GoogleDriveV1(baseDescription),
			2: new GoogleDriveV1(baseDescription),
			3: new GoogleDriveV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
