"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Teams/MicrosoftTeams.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Teams 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/MicrosoftTeamsV1.node、./v2/MicrosoftTeamsV2.node。导出:MicrosoftTeams。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Teams/MicrosoftTeams.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Teams/MicrosoftTeams_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { MicrosoftTeamsV1 } from './v1/MicrosoftTeamsV1.node';
import { MicrosoftTeamsV2 } from './v2/MicrosoftTeamsV2.node';

export class MicrosoftTeams extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Microsoft Teams',
			name: 'microsoftTeams',
			icon: 'file:teams.svg',
			group: ['input'],
			description: 'Consume Microsoft Teams API',
			defaultVersion: 2,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new MicrosoftTeamsV1(baseDescription),
			1.1: new MicrosoftTeamsV1(baseDescription),
			2: new MicrosoftTeamsV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
