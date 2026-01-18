"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Twitter/Twitter.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Twitter 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./V1/TwitterV1.node、./V2/TwitterV2.node。导出:Twitter。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Twitter/Twitter.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Twitter/Twitter_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { TwitterV1 } from './V1/TwitterV1.node';
import { TwitterV2 } from './V2/TwitterV2.node';

export class Twitter extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'X (Formerly Twitter)',
			name: 'twitter',
			icon: { light: 'file:x.svg', dark: 'file:x.dark.svg' },
			group: ['output'],
			subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
			description: 'Consume the X API',
			defaultVersion: 2,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new TwitterV1(baseDescription),
			2: new TwitterV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
