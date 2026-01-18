"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/comment/deleteComment.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../../descriptions、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/comment/deleteComment.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/comment/deleteComment_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '@utils/utilities';

import { commentRLC } from '../../descriptions';
import { theHiveApiRequest } from '../../transport';

const properties: INodeProperties[] = [commentRLC];

const displayOptions = {
	show: {
		resource: ['comment'],
		operation: ['deleteComment'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const commentId = this.getNodeParameter('commentId', i, '', { extractValue: true }) as string;

	await theHiveApiRequest.call(this, 'DELETE', `/v1/comment/${commentId}`);

	const executionData = this.helpers.constructExecutionMetaData(wrapData({ success: true }), {
		itemData: { item: i },
	});

	return executionData;
}
