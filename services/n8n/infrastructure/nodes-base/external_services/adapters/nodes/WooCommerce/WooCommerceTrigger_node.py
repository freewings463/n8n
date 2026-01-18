"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/WooCommerce/WooCommerceTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/WooCommerce 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:WooCommerceTrigger。关键函数/方法:create、delete、checkExists、webhook。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/WooCommerce/WooCommerceTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/WooCommerce/WooCommerceTrigger_node.py

import { createHmac } from 'crypto';
import type {
	IHookFunctions,
	IWebhookFunctions,
	IDataObject,
	INodeType,
	INodeTypeDescription,
	IWebhookResponseData,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { getAutomaticSecret, woocommerceApiRequest } from './GenericFunctions';

export class WooCommerceTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'WooCommerce Trigger',
		name: 'wooCommerceTrigger',
		icon: 'file:wooCommerce.svg',
		group: ['trigger'],
		version: 1,
		description: 'Handle WooCommerce events via webhooks',
		defaults: {
			name: 'WooCommerce Trigger',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'wooCommerceApi',
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
						name: 'coupon.created',
						value: 'coupon.created',
					},
					{
						name: 'coupon.deleted',
						value: 'coupon.deleted',
					},
					{
						name: 'coupon.updated',
						value: 'coupon.updated',
					},
					{
						name: 'customer.created',
						value: 'customer.created',
					},
					{
						name: 'customer.deleted',
						value: 'customer.deleted',
					},
					{
						name: 'customer.updated',
						value: 'customer.updated',
					},
					{
						name: 'order.created',
						value: 'order.created',
					},
					{
						name: 'order.deleted',
						value: 'order.deleted',
					},
					{
						name: 'order.updated',
						value: 'order.updated',
					},
					{
						name: 'product.created',
						value: 'product.created',
					},
					{
						name: 'product.deleted',
						value: 'product.deleted',
					},
					{
						name: 'product.updated',
						value: 'product.updated',
					},
				],
				description: 'Determines which resource events the webhook is triggered for',
			},
		],
	};

	webhookMethods = {
		default: {
			async checkExists(this: IHookFunctions): Promise<boolean> {
				const webhookUrl = this.getNodeWebhookUrl('default');
				const webhookData = this.getWorkflowStaticData('node');
				const currentEvent = this.getNodeParameter('event') as string;
				const endpoint = '/webhooks';

				const webhooks = await woocommerceApiRequest.call(
					this,
					'GET',
					endpoint,
					{},
					{ status: 'active', per_page: 100 },
				);

				for (const webhook of webhooks) {
					if (
						webhook.status === 'active' &&
						webhook.delivery_url === webhookUrl &&
						webhook.topic === currentEvent
					) {
						webhookData.webhookId = webhook.id;
						return true;
					}
				}
				return false;
			},
			async create(this: IHookFunctions): Promise<boolean> {
				const credentials = await this.getCredentials('wooCommerceApi');
				const webhookUrl = this.getNodeWebhookUrl('default');
				const webhookData = this.getWorkflowStaticData('node');
				const event = this.getNodeParameter('event') as string;
				const secret = getAutomaticSecret(credentials);
				const endpoint = '/webhooks';
				const body: IDataObject = {
					delivery_url: webhookUrl,
					topic: event,
					secret,
				};
				const { id } = await woocommerceApiRequest.call(this, 'POST', endpoint, body);
				webhookData.webhookId = id;
				webhookData.secret = secret;
				return true;
			},
			async delete(this: IHookFunctions): Promise<boolean> {
				const webhookData = this.getWorkflowStaticData('node');
				const endpoint = `/webhooks/${webhookData.webhookId}`;
				try {
					await woocommerceApiRequest.call(this, 'DELETE', endpoint, {}, { force: true });
				} catch (error) {
					return false;
				}
				delete webhookData.webhookId;
				delete webhookData.secret;
				return true;
			},
		},
	};

	async webhook(this: IWebhookFunctions): Promise<IWebhookResponseData> {
		const req = this.getRequestObject();
		const headerData = this.getHeaderData();
		const webhookData = this.getWorkflowStaticData('node');
		if (headerData['x-wc-webhook-id'] === undefined) {
			return {};
		}

		const computedSignature = createHmac('sha256', webhookData.secret as string)
			.update(req.rawBody)
			.digest('base64');
		if (headerData['x-wc-webhook-signature'] !== computedSignature) {
			// Signature is not valid so ignore call
			return {};
		}
		return {
			workflowData: [this.helpers.returnJsonArray(req.body as IDataObject)],
		};
	}
}
