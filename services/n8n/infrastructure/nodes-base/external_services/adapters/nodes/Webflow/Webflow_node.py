"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Webflow/Webflow.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Webflow 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./V1/WebflowV1.node、./V2/WebflowV2.node。导出:Webflow。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Webflow/Webflow.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Webflow/Webflow_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { WebflowV1 } from './V1/WebflowV1.node';
import { WebflowV2 } from './V2/WebflowV2.node';

export class Webflow extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Webflow',
			name: 'webflow',
			icon: 'file:webflow.svg',
			group: ['transform'],
			subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
			description: 'Consume the Webflow API',
			defaultVersion: 2,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new WebflowV1(baseDescription),
			2: new WebflowV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
