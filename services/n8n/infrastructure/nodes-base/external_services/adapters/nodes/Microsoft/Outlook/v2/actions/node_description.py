"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/node.description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./calendar、./contact、./draft、./event 等6项。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/node.description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/actions/node_description.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import { NodeConnectionTypes, type INodeTypeDescription } from 'n8n-workflow';

import * as calendar from './calendar';
import * as contact from './contact';
import * as draft from './draft';
import * as event from './event';
import * as folder from './folder';
import * as folderMessage from './folderMessage';
import * as message from './message';
import * as messageAttachment from './messageAttachment';
import { sendAndWaitWebhooksDescription } from '../../../../../utils/sendAndWait/descriptions';
import { SEND_AND_WAIT_WAITING_TOOLTIP } from '../../../../../utils/sendAndWait/utils';

export const description: INodeTypeDescription = {
	displayName: 'Microsoft Outlook',
	name: 'microsoftOutlook',
	group: ['transform'],
	icon: 'file:outlook.svg',
	version: 2,
	subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
	description: 'Consume Microsoft Outlook API',
	defaults: {
		name: 'Microsoft Outlook',
	},
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	usableAsTool: true,
	credentials: [
		{
			name: 'microsoftOutlookOAuth2Api',
			required: true,
		},
	],
	waitingNodeTooltip: SEND_AND_WAIT_WAITING_TOOLTIP,
	webhooks: sendAndWaitWebhooksDescription,
	properties: [
		{
			displayName: 'Resource',
			name: 'resource',
			type: 'options',
			noDataExpression: true,
			default: 'message',
			options: [
				{
					name: 'Calendar',
					value: 'calendar',
				},
				{
					name: 'Contact',
					value: 'contact',
				},
				{
					name: 'Draft',
					value: 'draft',
				},
				{
					name: 'Event',
					value: 'event',
				},
				{
					name: 'Folder',
					value: 'folder',
				},
				{
					name: 'Folder Message',
					value: 'folderMessage',
				},
				{
					name: 'Message',
					value: 'message',
				},
				{
					name: 'Message Attachment',
					value: 'messageAttachment',
				},
			],
		},
		...calendar.description,
		...contact.description,
		...draft.description,
		...event.description,
		...folder.description,
		...folderMessage.description,
		...message.description,
		...messageAttachment.description,
	],
};
