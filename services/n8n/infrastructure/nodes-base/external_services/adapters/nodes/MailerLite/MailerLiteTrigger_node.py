"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MailerLite/MailerLiteTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MailerLite 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/MailerLiteTriggerV1.node、./v2/MailerLiteTriggerV2.node。导出:MailerLiteTrigger。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MailerLite/MailerLiteTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MailerLite/MailerLiteTrigger_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { MailerLiteTriggerV1 } from './v1/MailerLiteTriggerV1.node';
import { MailerLiteTriggerV2 } from './v2/MailerLiteTriggerV2.node';

export class MailerLiteTrigger extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'MailerLite Trigger',
			name: 'mailerLiteTrigger',
			icon: 'file:MailerLite.svg',
			group: ['trigger'],
			description: 'Starts the workflow when MailerLite events occur',
			defaultVersion: 2,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new MailerLiteTriggerV1(baseDescription),
			2: new MailerLiteTriggerV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
