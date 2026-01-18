"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mailjet/MailjetTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mailjet 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:MailjetTrigger。关键函数/方法:create、delete、checkExists、webhook。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mailjet/MailjetTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mailjet/MailjetTrigger_node.py

import type {
	IHookFunctions,
	IWebhookFunctions,
	IDataObject,
	INodeType,
	INodeTypeDescription,
	IWebhookResponseData,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { mailjetApiRequest } from './GenericFunctions';

export class MailjetTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Mailjet Trigger',
		name: 'mailjetTrigger',
		icon: 'file:mailjet.svg',
		group: ['trigger'],
		version: 1,
		description: 'Handle Mailjet events via webhooks',
		defaults: {
			name: 'Mailjet Trigger',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'mailjetEmailApi',
				required: true,
			},
		],
		webhooks: [
			{
				name: 'default',
				httpMethod: 'POST',
				responseMode: 'onReceived',
				path: 'webhook',
			},
		],
		properties: [
			{
				displayName: 'Event',
				name: 'event',
				type: 'options',
				required: true,
				default: 'open',
				options: [
					{
						name: 'email.blocked',
						value: 'blocked',
					},
					{
						name: 'email.bounce',
						value: 'bounce',
					},
					{
						name: 'email.open',
						value: 'open',
					},
					{
						name: 'email.sent',
						value: 'sent',
					},
					{
						name: 'email.spam',
						value: 'spam',
					},
					{
						name: 'email.unsub',
						value: 'unsub',
					},
				],
				description: 'Determines which resource events the webhook is triggered for',
			},
		],
	};

	webhookMethods = {
		default: {
			async checkExists(this: IHookFunctions): Promise<boolean> {
				const endpoint = '/v3/rest/eventcallbackurl';
				const responseData = await mailjetApiRequest.call(this, 'GET', endpoint);

				const event = this.getNodeParameter('event') as string;
				const webhookUrl = this.getNodeWebhookUrl('default');

				for (const webhook of responseData.Data) {
					if (webhook.EventType === event && webhook.Url === webhookUrl) {
						// Set webhook-id to be sure that it can be deleted
						const webhookData = this.getWorkflowStaticData('node');
						webhookData.webhookId = webhook.ID as string;
						return true;
					}
				}

				return false;
			},
			async create(this: IHookFunctions): Promise<boolean> {
				const webhookUrl = this.getNodeWebhookUrl('default');
				const webhookData = this.getWorkflowStaticData('node');
				const event = this.getNodeParameter('event') as string;
				const endpoint = '/v3/rest/eventcallbackurl';
				const body: IDataObject = {
					Url: webhookUrl,
					EventType: event,
					Status: 'alive',
					isBackup: 'false',
				};
				const { Data } = await mailjetApiRequest.call(this, 'POST', endpoint, body);
				webhookData.webhookId = Data[0].ID;
				return true;
			},
			async delete(this: IHookFunctions): Promise<boolean> {
				const webhookData = this.getWorkflowStaticData('node');
				const endpoint = `/v3/rest/eventcallbackurl/${webhookData.webhookId}`;
				try {
					await mailjetApiRequest.call(this, 'DELETE', endpoint);
				} catch (error) {
					return false;
				}
				delete webhookData.webhookId;
				return true;
			},
		},
	};

	async webhook(this: IWebhookFunctions): Promise<IWebhookResponseData> {
		const req = this.getRequestObject();
		return {
			workflowData: [this.helpers.returnJsonArray(req.body as IDataObject[])],
		};
	}
}
