"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/chatMessage/sendAndWait.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Teams 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../utils/utilities、../../descriptions、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/chatMessage/sendAndWait.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Teams/v2/actions/chatMessage/sendAndWait_operation.py

import type { INodeProperties, IExecuteFunctions } from 'n8n-workflow';

import {
	getSendAndWaitConfig,
	getSendAndWaitProperties,
} from '../../../../../../utils/sendAndWait/utils';
import { createUtmCampaignLink } from '../../../../../../utils/utilities';
import { chatRLC } from '../../descriptions';
import { microsoftApiRequest } from '../../transport';

export const description: INodeProperties[] = getSendAndWaitProperties(
	[chatRLC],
	'chatMessage',
	undefined,
	{
		noButtonStyle: true,
		defaultApproveLabel: '✓ Approve',
		defaultDisapproveLabel: '✗ Decline',
	},
).filter((p) => p.name !== 'subject');

export async function execute(this: IExecuteFunctions, i: number, instanceId: string) {
	const chatId = this.getNodeParameter('chatId', i, '', { extractValue: true }) as string;
	const config = getSendAndWaitConfig(this);

	const buttons = config.options.map((option) => `<a href="${option.url}">${option.label}</a>`);

	let content = `${config.message}<br><br>${buttons.join(' ')}`;

	if (config.appendAttribution !== false) {
		const attributionText = 'This message was sent automatically with';
		const link = createUtmCampaignLink('n8n-nodes-base.microsoftTeams', instanceId);
		const attribution = `<em>${attributionText} <a href="${link}">n8n</a></em>`;
		content += `<br><br>${attribution}`;
	}

	const body = {
		body: {
			contentType: 'html',
			content,
		},
	};

	return await microsoftApiRequest.call(this, 'POST', `/v1.0/chats/${chatId}/messages`, body);
}
