"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Sheet/GoogleSheets.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Sheet 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/GoogleSheetsV1.node、./v2/GoogleSheetsV2.node。导出:GoogleSheets。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Sheet/GoogleSheets.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Sheet/GoogleSheets_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { GoogleSheetsV1 } from './v1/GoogleSheetsV1.node';
import { GoogleSheetsV2 } from './v2/GoogleSheetsV2.node';

export class GoogleSheets extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Google Sheets',
			name: 'googleSheets',
			icon: 'file:googleSheets.svg',
			group: ['input', 'output'],
			defaultVersion: 4.7,
			subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
			description: 'Read, update and write data to Google Sheets',
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new GoogleSheetsV1(baseDescription),
			2: new GoogleSheetsV1(baseDescription),
			3: new GoogleSheetsV2(baseDescription),
			4: new GoogleSheetsV2(baseDescription),
			4.1: new GoogleSheetsV2(baseDescription),
			4.2: new GoogleSheetsV2(baseDescription),
			4.3: new GoogleSheetsV2(baseDescription),
			4.4: new GoogleSheetsV2(baseDescription),
			4.5: new GoogleSheetsV2(baseDescription),
			4.6: new GoogleSheetsV2(baseDescription),
			4.7: new GoogleSheetsV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
