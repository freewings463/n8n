"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mautic/MauticTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mautic 的节点。导入/依赖:外部:无；内部:无；本地:./GenericFunctions。导出:MauticTrigger。关键函数/方法:create、delete、getEvents、eventName、eventDecription、checkExists、webhook。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mautic/MauticTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mautic/MauticTrigger_node.py

import {
	type IHookFunctions,
	type IWebhookFunctions,
	type IDataObject,
	type ILoadOptionsFunctions,
	type INodePropertyOptions,
	type INodeType,
	type INodeTypeDescription,
	type IWebhookResponseData,
	NodeConnectionTypes,
} from 'n8n-workflow';
import { parse as urlParse } from 'url';

import { mauticApiRequest } from './GenericFunctions';

export class MauticTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Mautic Trigger',
		name: 'mauticTrigger',
		icon: 'file:mautic.svg',
		group: ['trigger'],
		version: 1,
		description: 'Handle Mautic events via webhooks',
		defaults: {
			name: 'Mautic Trigger',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'mauticApi',
				required: true,
				displayOptions: {
					show: {
						authentication: ['credentials'],
					},
				},
			},
			{
				name: 'mauticOAuth2Api',
				required: true,
				displayOptions: {
					show: {
						authentication: ['oAuth2'],
					},
				},
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
				displayName: 'Authentication',
				name: 'authentication',
				type: 'options',
				options: [
					{
						name: 'Credentials',
						value: 'credentials',
					},
					{
						name: 'OAuth2',
						value: 'oAuth2',
					},
				],
				default: 'credentials',
			},
			{
				displayName: 'Event Names or IDs',
				name: 'events',
				type: 'multiOptions',
				description:
					'Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				required: true,
				typeOptions: {
					loadOptionsMethod: 'getEvents',
				},
				default: [],
			},
			{
				displayName: 'Events Order',
				name: 'eventsOrder',
				type: 'options',
				default: 'ASC',
				options: [
					{
						name: 'ASC',
						value: 'ASC',
					},
					{
						name: 'DESC',
						value: 'DESC',
					},
				],
				description: 'Order direction for queued events in one webhook. Can be “DESC” or “ASC”.',
			},
		],
	};

	methods = {
		loadOptions: {
			// Get all the events to display them to user so that they can
			// select them easily
			async getEvents(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				const returnData: INodePropertyOptions[] = [];
				const { triggers } = await mauticApiRequest.call(this, 'GET', '/hooks/triggers');
				for (const [key, value] of Object.entries(triggers as IDataObject)) {
					const eventId = key;
					const eventName = (value as IDataObject).label as string;
					const eventDecription = (value as IDataObject).description as string;
					returnData.push({
						name: eventName,
						value: eventId,
						description: eventDecription,
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
				const endpoint = `/hooks/${webhookData.webhookId}`;
				try {
					await mauticApiRequest.call(this, 'GET', endpoint, {});
				} catch (error) {
					return false;
				}
				return true;
			},
			async create(this: IHookFunctions): Promise<boolean> {
				const webhookUrl = this.getNodeWebhookUrl('default') as string;
				const webhookData = this.getWorkflowStaticData('node');
				const events = this.getNodeParameter('events', 0) as string[];
				const eventsOrder = this.getNodeParameter('eventsOrder', 0) as string;
				const urlParts = urlParse(webhookUrl);
				const body: IDataObject = {
					name: `n8n-webhook:${urlParts.path}`,
					description: 'n8n webhook',
					webhookUrl,
					triggers: events,
					eventsOrderbyDir: eventsOrder,
					isPublished: true,
				};
				const { hook } = await mauticApiRequest.call(this, 'POST', '/hooks/new', body);
				webhookData.webhookId = hook.id;
				return true;
			},
			async delete(this: IHookFunctions): Promise<boolean> {
				const webhookData = this.getWorkflowStaticData('node');
				try {
					await mauticApiRequest.call(this, 'DELETE', `/hooks/${webhookData.webhookId}/delete`);
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
			workflowData: [this.helpers.returnJsonArray(req.body as IDataObject)],
		};
	}
}
