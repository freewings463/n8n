"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/draft/send.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../../descriptions、../helpers/utils、../../transport。导出:properties、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/draft/send.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/actions/draft/send_operation.py

import type { IExecuteFunctions, INodeProperties } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { draftRLC } from '../../descriptions';
import { makeRecipient } from '../../helpers/utils';
import { microsoftApiRequest } from '../../transport';

export const properties: INodeProperties[] = [
	draftRLC,
	{
		displayName: 'To',
		name: 'to',
		description: 'Comma-separated list of email addresses of recipients',
		type: 'string',
		default: '',
	},
];

const displayOptions = {
	show: {
		resource: ['draft'],
		operation: ['send'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, index: number) {
	const draftId = this.getNodeParameter('draftId', index, undefined, { extractValue: true });
	const to = this.getNodeParameter('to', index) as string;

	if (to) {
		const recipients = to
			.split(',')
			.map((s) => s.trim())
			.filter((email) => email);

		if (recipients.length !== 0) {
			await microsoftApiRequest.call(this, 'PATCH', `/messages/${draftId}`, {
				toRecipients: recipients.map((recipient: string) => makeRecipient(recipient)),
			});
		}
	}

	await microsoftApiRequest.call(this, 'POST', `/messages/${draftId}/send`);

	const executionData = this.helpers.constructExecutionMetaData(
		this.helpers.returnJsonArray({ success: true }),
		{ itemData: { item: index } },
	);

	return executionData;
}
