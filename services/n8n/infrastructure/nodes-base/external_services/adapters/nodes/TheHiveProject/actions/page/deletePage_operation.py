"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/page/deletePage.operation.ts
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
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/page/deletePage.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/page/deletePage_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '@utils/utilities';

import { caseRLC, pageRLC } from '../../descriptions';
import { theHiveApiRequest } from '../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Delete From ...',
		name: 'location',
		type: 'options',
		options: [
			{
				name: 'Case',
				value: 'case',
			},
			{
				name: 'Knowledge Base',
				value: 'knowledgeBase',
			},
		],
		default: 'knowledgeBase',
	},
	{
		...caseRLC,
		displayOptions: {
			show: {
				location: ['case'],
			},
		},
	},
	pageRLC,
];

const displayOptions = {
	show: {
		resource: ['page'],
		operation: ['deletePage'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const location = this.getNodeParameter('location', i) as string;
	const pageId = this.getNodeParameter('pageId', i, '', { extractValue: true }) as string;

	let endpoint;

	if (location === 'case') {
		const caseId = this.getNodeParameter('caseId', i, '', { extractValue: true }) as string;
		endpoint = `/v1/case/${caseId}/page/${pageId}`;
	} else {
		endpoint = `/v1/page/${pageId}`;
	}

	await theHiveApiRequest.call(this, 'DELETE', endpoint);

	const executionData = this.helpers.constructExecutionMetaData(wrapData({ success: true }), {
		itemData: { item: i },
	});

	return executionData;
}
