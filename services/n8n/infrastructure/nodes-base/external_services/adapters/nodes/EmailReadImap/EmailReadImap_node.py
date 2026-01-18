"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/EmailReadImap/EmailReadImap.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/EmailReadImap 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/EmailReadImapV1.node、./v2/EmailReadImapV2.node。导出:EmailReadImap。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/EmailReadImap/EmailReadImap.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/EmailReadImap/EmailReadImap_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { EmailReadImapV1 } from './v1/EmailReadImapV1.node';
import { EmailReadImapV2 } from './v2/EmailReadImapV2.node';

export class EmailReadImap extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Email Trigger (IMAP)',
			name: 'emailReadImap',
			icon: 'fa:inbox',
			group: ['trigger'],
			description: 'Triggers the workflow when a new email is received',
			defaultVersion: 2.1,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new EmailReadImapV1(baseDescription),
			2: new EmailReadImapV2(baseDescription),
			2.1: new EmailReadImapV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
