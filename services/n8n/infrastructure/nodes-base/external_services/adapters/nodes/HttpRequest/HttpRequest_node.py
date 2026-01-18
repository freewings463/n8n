"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HttpRequest/HttpRequest.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HttpRequest 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./V1/HttpRequestV1.node、./V2/HttpRequestV2.node、./V3/HttpRequestV3.node。导出:HttpRequest。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HttpRequest/HttpRequest.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HttpRequest/HttpRequest_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { HttpRequestV1 } from './V1/HttpRequestV1.node';
import { HttpRequestV2 } from './V2/HttpRequestV2.node';
import { HttpRequestV3 } from './V3/HttpRequestV3.node';

export class HttpRequest extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'HTTP Request',
			name: 'httpRequest',
			icon: { light: 'file:httprequest.svg', dark: 'file:httprequest.dark.svg' },
			group: ['output'],
			subtitle: '={{$parameter["requestMethod"] + ": " + $parameter["url"]}}',
			description: 'Makes an HTTP request and returns the response data',
			defaultVersion: 4.3,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new HttpRequestV1(baseDescription),
			2: new HttpRequestV2(baseDescription),
			3: new HttpRequestV3(baseDescription),
			4: new HttpRequestV3(baseDescription),
			4.1: new HttpRequestV3(baseDescription),
			4.2: new HttpRequestV3(baseDescription),
			4.3: new HttpRequestV3(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
