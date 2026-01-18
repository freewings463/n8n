"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Analytics/GoogleAnalytics.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Analytics 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/GoogleAnalyticsV1.node、./v2/GoogleAnalyticsV2.node。导出:GoogleAnalytics。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Analytics/GoogleAnalytics.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Analytics/GoogleAnalytics_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { GoogleAnalyticsV1 } from './v1/GoogleAnalyticsV1.node';
import { GoogleAnalyticsV2 } from './v2/GoogleAnalyticsV2.node';

export class GoogleAnalytics extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Google Analytics',
			name: 'googleAnalytics',
			icon: 'file:analytics.svg',
			group: ['transform'],
			subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
			description: 'Use the Google Analytics API',
			defaultVersion: 2,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new GoogleAnalyticsV1(baseDescription),
			2: new GoogleAnalyticsV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
