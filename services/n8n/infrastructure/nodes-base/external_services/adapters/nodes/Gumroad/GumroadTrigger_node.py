"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Gumroad/GumroadTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Gumroad 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:GumroadTrigger。关键函数/方法:create、delete、checkExists、webhook。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Gumroad/GumroadTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Gumroad/GumroadTrigger_node.py

import type {
	IHookFunctions,
	IWebhookFunctions,
	IDataObject,
	INodeType,
	INodeTypeDescription,
	IWebhookResponseData,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { gumroadApiRequest } from './GenericFunctions';

export class GumroadTrigger implements INodeType {
	// eslint-disable-next-line n8n-nodes-base/node-class-description-missing-subtitle
	description: INodeTypeDescription = {
		displayName: 'Gumroad Trigger',
		name: 'gumroadTrigger',
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:gumroad.png',
		group: ['trigger'],
		version: 1,
		description: 'Handle Gumroad events via webhooks',
		defaults: {
			name: 'Gumroad Trigger',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'gumroadApi',
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
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				required: true,
				default: '',
				options: [
					{
						name: 'Cancellation',
						value: 'cancellation',
						description:
							"When subscribed to this resource, you will be notified of cancellations of the user's subscribers",
					},
					{
						name: 'Dispute',
						value: 'dispute',
						description:
							"When subscribed to this resource, you will be notified of the disputes raised against user's sales",
					},
					{
						name: 'Dispute Won',
						value: 'dispute_won',
						description:
							'When subscribed to this resource, you will be notified of the sale disputes won',
					},
					{
						name: 'Refund',
						value: 'refund',
						description:
							"When subscribed to this resource, you will be notified of refunds to the user's sales",
					},
					{
						name: 'Sale',
						value: 'sale',
						description:
							"When subscribed to this resource, you will be notified of the user's sales",
					},
				],
				description: 'The resource is gonna fire the event',
			},
		],
	};

	webhookMethods = {
		default: {
			async checkExists(this: IHookFunctions): Promise<boolean> {
				const webhookData = this.getWorkflowStaticData('node');
				if (webhookData.webhookId === undefined) {
					return false;
				}
				const endpoint = '/resource_subscriptions';
				const { resource_subscriptions } = await gumroadApiRequest.call(this, 'GET', endpoint);
				if (Array.isArray(resource_subscriptions)) {
					for (const resource of resource_subscriptions) {
						if (resource.id === webhookData.webhookId) {
							return true;
						}
					}
				}
				return false;
			},
			async create(this: IHookFunctions): Promise<boolean> {
				const webhookUrl = this.getNodeWebhookUrl('default');
				const webhookData = this.getWorkflowStaticData('node');
				const resource = this.getNodeParameter('resource') as string;
				const endpoint = '/resource_subscriptions';
				const body: IDataObject = {
					post_url: webhookUrl,
					resource_name: resource,
				};
				const { resource_subscription } = await gumroadApiRequest.call(this, 'PUT', endpoint, body);
				webhookData.webhookId = resource_subscription.id;
				return true;
			},
			async delete(this: IHookFunctions): Promise<boolean> {
				let responseData;
				const webhookData = this.getWorkflowStaticData('node');
				const endpoint = `/resource_subscriptions/${webhookData.webhookId}`;
				try {
					responseData = await gumroadApiRequest.call(this, 'DELETE', endpoint);
				} catch (error) {
					return false;
				}
				if (!responseData.success) {
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
			workflowData: [this.helpers.returnJsonArray(req.body as IDataObject)],
		};
	}
}
