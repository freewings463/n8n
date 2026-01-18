"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DateTime/DateTime.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DateTime 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./V1/DateTimeV1.node、./V2/DateTimeV2.node。导出:DateTime。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DateTime/DateTime.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DateTime/DateTime_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { DateTimeV1 } from './V1/DateTimeV1.node';
import { DateTimeV2 } from './V2/DateTimeV2.node';

export class DateTime extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Date & Time',
			name: 'dateTime',
			icon: 'fa:clock',
			iconColor: 'green',
			group: ['transform'],
			defaultVersion: 2,
			description: 'Allows you to manipulate date and time values',
			subtitle: '={{$parameter["action"]}}',
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new DateTimeV1(baseDescription),
			2: new DateTimeV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
