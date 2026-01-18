"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Keap/KeapTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Keap 的节点。导入/依赖:外部:change-case；内部:n8n-workflow；本地:./GenericFunctions。导出:KeapTrigger。关键函数/方法:create、delete、getEvents、checkExists、webhook。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Keap/KeapTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Keap/KeapTrigger_node.py

import { capitalCase } from 'change-case';
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

import { keapApiRequest } from './GenericFunctions';

export class KeapTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Keap Trigger',
		name: 'keapTrigger',
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:keap.png',
		group: ['trigger'],
		version: 1,
		subtitle: '={{$parameter["eventId"]}}',
		description: 'Starts the workflow when Infusionsoft events occur',
		defaults: {
			name: 'Keap Trigger',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'keapOAuth2Api',
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
				displayName: 'Event Name or ID',
				name: 'eventId',
				type: 'options',
				description:
					'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				typeOptions: {
					loadOptionsMethod: 'getEvents',
				},
				default: '',
				required: true,
			},
			{
				displayName: 'RAW Data',
				name: 'rawData',
				type: 'boolean',
				default: false,
				description: 'Whether to return the data exactly in the way it got received from the API',
			},
		],
	};

	methods = {
		loadOptions: {
			// Get all the event types to display them to user so that they can
			// select them easily
			async getEvents(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				const returnData: INodePropertyOptions[] = [];
				const hooks = await keapApiRequest.call(this, 'GET', '/hooks/event_keys');
				for (const hook of hooks) {
					const hookName = hook;
					const hookId = hook;
					returnData.push({
						name: capitalCase((hookName as string).replace('.', ' ')),
						value: hookId as string,
					});
				}
				return returnData;
			},
		},
	};

	webhookMethods = {
		default: {
			async checkExists(this: IHookFunctions): Promise<boolean> {
				const eventId = this.getNodeParameter('eventId') as string;
				const webhookUrl = this.getNodeWebhookUrl('default');
				const webhookData = this.getWorkflowStaticData('node');

				const responseData = await keapApiRequest.call(this, 'GET', '/hooks', {});

				for (const existingData of responseData) {
					if (
						existingData.hookUrl === webhookUrl &&
						existingData.eventKey === eventId &&
						existingData.status === 'Verified'
					) {
						// The webhook exists already
						webhookData.webhookId = existingData.key;
						return true;
					}
				}

				return false;
			},
			async create(this: IHookFunctions): Promise<boolean> {
				const eventId = this.getNodeParameter('eventId') as string;
				const webhookData = this.getWorkflowStaticData('node');
				const webhookUrl = this.getNodeWebhookUrl('default');

				const body = {
					eventKey: eventId,
					hookUrl: webhookUrl,
				};

				const responseData = await keapApiRequest.call(this, 'POST', '/hooks', body);

				if (responseData.key === undefined) {
					// Required data is missing so was not successful
					return false;
				}

				webhookData.webhookId = responseData.key as string;

				return true;
			},
			async delete(this: IHookFunctions): Promise<boolean> {
				const webhookData = this.getWorkflowStaticData('node');

				if (webhookData.webhookId !== undefined) {
					try {
						await keapApiRequest.call(this, 'DELETE', `/hooks/${webhookData.webhookId}`);
					} catch (error) {
						return false;
					}

					// Remove from the static workflow data so that it is clear
					// that no webhooks are registered anymore
					delete webhookData.webhookId;
				}

				return true;
			},
		},
	};

	async webhook(this: IWebhookFunctions): Promise<IWebhookResponseData> {
		const rawData = this.getNodeParameter('rawData') as boolean;
		const headers = this.getHeaderData() as IDataObject;
		const bodyData = this.getBodyData();

		if (headers['x-hook-secret']) {
			// Is a create webhook confirmation request
			const res = this.getResponseObject();
			res.set('x-hook-secret', headers['x-hook-secret'] as string);
			res.status(200).end();
			return {
				noWebhookResponse: true,
			};
		}

		if (rawData) {
			return {
				workflowData: [this.helpers.returnJsonArray(bodyData)],
			};
		}

		const responseData: IDataObject[] = [];
		for (const data of bodyData.object_keys as IDataObject[]) {
			responseData.push({
				eventKey: bodyData.event_key,
				objectType: bodyData.object_type,
				id: data.id,
				timestamp: data.timestamp,
				apiUrl: data.apiUrl,
			});
		}
		return {
			workflowData: [this.helpers.returnJsonArray(responseData)],
		};
	}
}
