"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Autopilot/AutopilotTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Autopilot 的节点。导入/依赖:外部:change-case；内部:n8n-workflow；本地:./GenericFunctions。导出:AutopilotTrigger。关键函数/方法:create、delete、checkExists、webhook。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Autopilot/AutopilotTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Autopilot/AutopilotTrigger_node.py

import { snakeCase } from 'change-case';
import type {
	IHookFunctions,
	IWebhookFunctions,
	IDataObject,
	INodeType,
	INodeTypeDescription,
	IWebhookResponseData,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { autopilotApiRequest } from './GenericFunctions';

export class AutopilotTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Autopilot Trigger',
		name: 'autopilotTrigger',
		icon: 'file:autopilot.svg',
		group: ['trigger'],
		version: 1,
		subtitle: '={{$parameter["event"]}}',
		description: 'Handle Autopilot events via webhooks',
		defaults: {
			name: 'Autopilot Trigger',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'autopilotApi',
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
				default: '',
				options: [
					{
						name: 'Contact Added',
						value: 'contactAdded',
					},
					{
						name: 'Contact Added To List',
						value: 'contactAddedToList',
					},
					{
						name: 'Contact Entered Segment',
						value: 'contactEnteredSegment',
					},
					{
						name: 'Contact Left Segment',
						value: 'contactLeftSegment',
					},
					{
						name: 'Contact Removed From List',
						value: 'contactRemovedFromList',
					},
					{
						name: 'Contact Unsubscribed',
						value: 'contactUnsubscribed',
					},
					{
						name: 'Contact Updated',
						value: 'contactUpdated',
					},
				],
			},
		],
	};

	webhookMethods = {
		default: {
			async checkExists(this: IHookFunctions): Promise<boolean> {
				const webhookData = this.getWorkflowStaticData('node');
				const webhookUrl = this.getNodeWebhookUrl('default');
				const event = this.getNodeParameter('event') as string;
				const { hooks: webhooks } = await autopilotApiRequest.call(this, 'GET', '/hooks');
				for (const webhook of webhooks) {
					if (webhook.target_url === webhookUrl && webhook.event === snakeCase(event)) {
						webhookData.webhookId = webhook.hook_id;
						return true;
					}
				}
				return false;
			},
			async create(this: IHookFunctions): Promise<boolean> {
				const webhookUrl = this.getNodeWebhookUrl('default');
				const webhookData = this.getWorkflowStaticData('node');
				const event = this.getNodeParameter('event') as string;
				const body: IDataObject = {
					event: snakeCase(event),
					target_url: webhookUrl,
				};
				const webhook = await autopilotApiRequest.call(this, 'POST', '/hook', body);
				webhookData.webhookId = webhook.hook_id;
				return true;
			},
			async delete(this: IHookFunctions): Promise<boolean> {
				const webhookData = this.getWorkflowStaticData('node');
				try {
					await autopilotApiRequest.call(this, 'DELETE', `/hook/${webhookData.webhookId}`);
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
