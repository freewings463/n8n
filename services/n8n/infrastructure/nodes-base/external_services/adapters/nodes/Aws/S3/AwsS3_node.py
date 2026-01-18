"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/S3/AwsS3.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/S3 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./V1/AwsS3V1.node、./V2/AwsS3V2.node。导出:AwsS3。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/S3/AwsS3.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/S3/AwsS3_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { AwsS3V1 } from './V1/AwsS3V1.node';
import { AwsS3V2 } from './V2/AwsS3V2.node';

export class AwsS3 extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'AwsS3',
			name: 'awsS3',
			icon: 'file:s3.svg',
			group: ['output'],
			subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
			description: 'Sends data to AWS S3',
			defaultVersion: 2,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new AwsS3V1(baseDescription),
			2: new AwsS3V2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
