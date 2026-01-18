"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHive/TheHiveTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHive 的节点。导入/依赖:外部:无；内部:无；本地:./descriptions/EventsDescription。导出:TheHiveTrigger。关键函数/方法:create、delete、checkExists、webhook、operation。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHive/TheHiveTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHive/TheHiveTrigger_node.py

import {
	type IWebhookFunctions,
	type IDataObject,
	type IHookFunctions,
	type INodeType,
	type INodeTypeDescription,
	type IWebhookResponseData,
	NodeConnectionTypes,
} from 'n8n-workflow';

import { eventsDescription } from './descriptions/EventsDescription';

export class TheHiveTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'TheHive Trigger',
		name: 'theHiveTrigger',
		icon: 'file:thehive.svg',
		group: ['trigger'],
		version: [1, 2],
		description: 'Starts the workflow when TheHive events occur',
		defaults: {
			name: 'TheHive Trigger',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
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
				displayName:
					'You must set up the webhook in TheHive — instructions <a href="https://docs.n8n.io/integrations/builtin/trigger-nodes/n8n-nodes-base.thehivetrigger/#configure-a-webhook-in-thehive" target="_blank">here</a>',
				name: 'notice',
				type: 'notice',
				default: '',
			},
			...eventsDescription,
		],
	};

	webhookMethods = {
		default: {
			async checkExists(this: IHookFunctions): Promise<boolean> {
				return true;
			},
			async create(this: IHookFunctions): Promise<boolean> {
				return true;
			},
			async delete(this: IHookFunctions): Promise<boolean> {
				return true;
			},
		},
	};

	async webhook(this: IWebhookFunctions): Promise<IWebhookResponseData> {
		// Get the request body
		const bodyData = this.getBodyData();
		const events = this.getNodeParameter('events', []) as string[];
		if (!bodyData.operation || !bodyData.objectType) {
			// Don't start the workflow if mandatory fields are not specified
			return {};
		}

		// Don't start the workflow if the event is not fired
		// Replace Creation with Create for TheHive 3 support
		const operation = (bodyData.operation as string).replace('Creation', 'Create');
		const event = `${(bodyData.objectType as string).toLowerCase()}_${operation.toLowerCase()}`;

		if (events.indexOf('*') === -1 && events.indexOf(event) === -1) {
			return {};
		}

		// The data to return and so start the workflow with
		const returnData: IDataObject[] = [];
		returnData.push({
			event,
			body: this.getBodyData(),
			headers: this.getHeaderData(),
			query: this.getQueryData(),
		});

		return {
			workflowData: [this.helpers.returnJsonArray(returnData)],
		};
	}
}
