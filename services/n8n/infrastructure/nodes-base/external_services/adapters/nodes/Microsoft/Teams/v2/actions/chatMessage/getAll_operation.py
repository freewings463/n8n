"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/chatMessage/getAll.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Teams 的节点。导入/依赖:外部:@utils/descriptions、@utils/utilities；内部:n8n-workflow；本地:../../descriptions、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/chatMessage/getAll.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Teams/v2/actions/chatMessage/getAll_operation.py

import type { INodeProperties, IExecuteFunctions } from 'n8n-workflow';

import { returnAllOrLimit } from '@utils/descriptions';
import { updateDisplayOptions } from '@utils/utilities';

import { chatRLC } from '../../descriptions';
import { microsoftApiRequestAllItems } from '../../transport';

const properties: INodeProperties[] = [chatRLC, ...returnAllOrLimit];

const displayOptions = {
	show: {
		resource: ['chatMessage'],
		operation: ['getAll'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number) {
	// https://docs.microsoft.com/en-us/graph/api/chat-list-messages?view=graph-rest-1.0&tabs=http

	const chatId = this.getNodeParameter('chatId', i, '', { extractValue: true }) as string;
	const returnAll = this.getNodeParameter('returnAll', i);

	if (returnAll) {
		return await microsoftApiRequestAllItems.call(
			this,
			'value',
			'GET',
			`/v1.0/chats/${chatId}/messages`,
		);
	} else {
		const limit = this.getNodeParameter('limit', i);
		const responseData = await microsoftApiRequestAllItems.call(
			this,
			'value',
			'GET',
			`/v1.0/chats/${chatId}/messages`,
			{},
		);
		return responseData.splice(0, limit);
	}
}
