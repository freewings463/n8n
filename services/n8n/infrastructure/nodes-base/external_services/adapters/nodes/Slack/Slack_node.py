"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Slack/Slack.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Slack 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./V1/SlackV1.node、./V2/SlackV2.node。导出:Slack。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Slack/Slack.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Slack/Slack_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { SlackV1 } from './V1/SlackV1.node';
import { SlackV2 } from './V2/SlackV2.node';

export class Slack extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Slack',
			name: 'slack',
			icon: 'file:slack.svg',
			group: ['output'],
			subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
			description: 'Consume Slack API',
			defaultVersion: 2.4,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new SlackV1(baseDescription),
			2: new SlackV2(baseDescription),
			2.1: new SlackV2(baseDescription),
			2.2: new SlackV2(baseDescription),
			2.3: new SlackV2(baseDescription),
			2.4: new SlackV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
