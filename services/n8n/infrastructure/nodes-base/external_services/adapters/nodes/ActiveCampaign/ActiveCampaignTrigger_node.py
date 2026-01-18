"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActiveCampaign/ActiveCampaignTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActiveCampaign 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:ActiveCampaignTrigger。关键函数/方法:create、delete、getEvents、checkExists、webhook。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActiveCampaign/ActiveCampaignTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActiveCampaign/ActiveCampaignTrigger_node.py

import type {
	IHookFunctions,
	IWebhookFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	INodePropertyOptions,
	INodeType,
	INodeTypeDescription,
	IWebhookResponseData,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { activeCampaignApiRequest, activeCampaignApiRequestAllItems } from './GenericFunctions';

export class ActiveCampaignTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'ActiveCampaign Trigger',
		name: 'activeCampaignTrigger',
		icon: { light: 'file:activeCampaign.svg', dark: 'file:activeCampaign.dark.svg' },
		group: ['trigger'],
		version: 1,
		description: 'Handle ActiveCampaign events via webhooks',
		defaults: {
			name: 'ActiveCampaign Trigger',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'activeCampaignApi',
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
				displayName: 'Event Names or IDs',
				name: 'events',
				type: 'multiOptions',
				description:
					'Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				typeOptions: {
					loadOptionsMethod: 'getEvents',
				},
				default: [],
				options: [],
			},
			{
				displayName: 'Source',
				name: 'sources',
				type: 'multiOptions',
				options: [
					{
						name: 'Public',
						value: 'public',
						description: 'Run the hooks when a contact triggers the action',
					},
					{
						name: 'Admin',
						value: 'admin',
						description: 'Run the hooks when an admin user triggers the action',
					},
					{
						name: 'Api',
						value: 'api',
						description: 'Run the hooks when an API call triggers the action',
					},
					{
						name: 'System',
						value: 'system',
						description: 'Run the hooks when automated systems triggers the action',
					},
				],
				default: [],
			},
		],
	};

	methods = {
		loadOptions: {
			// Get all the events to display them to user so that they can
			// select them easily
			async getEvents(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				const returnData: INodePropertyOptions[] = [];
				const events = await activeCampaignApiRequestAllItems.call(
					this,
					'GET',
					'/api/3/webhook/events',
					{},
					{},
					'webhookEvents',
				);
				for (const event of events) {
					const eventName = event;
					const eventId = event;
					returnData.push({
						name: eventName,
						value: eventId,
					});
				}
				return returnData;
			},
		},
	};

	webhookMethods = {
		default: {
			async checkExists(this: IHookFunctions): Promise<boolean> {
				const webhookData = this.getWorkflowStaticData('node');
				if (webhookData.webhookId === undefined) {
					return false;
				}
				const endpoint = `/api/3/webhooks/${webhookData.webhookId}`;
				try {
					await activeCampaignApiRequest.call(this, 'GET', endpoint, {});
				} catch (error) {
					return false;
				}
				return true;
			},
			async create(this: IHookFunctions): Promise<boolean> {
				const webhookUrl = this.getNodeWebhookUrl('default') as string;
				const webhookData = this.getWorkflowStaticData('node');
				const events = this.getNodeParameter('events', []) as string[];
				const sources = this.getNodeParameter('sources', '') as string[];
				const body: IDataObject = {
					webhook: {
						name: `n8n-webhook:${webhookUrl}`,
						url: webhookUrl,
						events,
						sources,
					},
				};
				const { webhook } = await activeCampaignApiRequest.call(
					this,
					'POST',
					'/api/3/webhooks',
					body,
				);
				webhookData.webhookId = webhook.id;
				return true;
			},
			async delete(this: IHookFunctions): Promise<boolean> {
				const webhookData = this.getWorkflowStaticData('node');
				try {
					await activeCampaignApiRequest.call(
						this,
						'DELETE',
						`/api/3/webhooks/${webhookData.webhookId}`,
						{},
					);
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
