"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SpreadsheetFile/SpreadsheetFile.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SpreadsheetFile 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/SpreadsheetFileV1.node、./v2/SpreadsheetFileV2.node。导出:SpreadsheetFile。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SpreadsheetFile/SpreadsheetFile.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SpreadsheetFile/SpreadsheetFile_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { SpreadsheetFileV1 } from './v1/SpreadsheetFileV1.node';
import { SpreadsheetFileV2 } from './v2/SpreadsheetFileV2.node';

export class SpreadsheetFile extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			hidden: true,
			displayName: 'Spreadsheet File',
			name: 'spreadsheetFile',
			icon: 'fa:table',
			group: ['transform'],
			description: 'Reads and writes data from a spreadsheet file like CSV, XLS, ODS, etc',
			defaultVersion: 2,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new SpreadsheetFileV1(baseDescription),
			2: new SpreadsheetFileV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
