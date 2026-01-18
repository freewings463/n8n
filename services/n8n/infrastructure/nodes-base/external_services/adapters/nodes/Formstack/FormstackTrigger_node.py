"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Formstack/FormstackTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Formstack 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:FormstackTrigger。关键函数/方法:create、delete、checkExists、webhook。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Formstack/FormstackTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Formstack/FormstackTrigger_node.py

import type {
	IHookFunctions,
	IWebhookFunctions,
	IDataObject,
	INodeType,
	INodeTypeDescription,
	IWebhookResponseData,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import type { IFormstackWebhookResponseBody } from './GenericFunctions';
import { apiRequest, getForms } from './GenericFunctions';

export class FormstackTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Formstack Trigger',
		name: 'formstackTrigger',
		icon: 'file:formstack.svg',
		group: ['trigger'],
		version: 1,
		subtitle: '=Form ID: {{$parameter["formId"]}}',
		description: 'Starts the workflow on a Formstack form submission.',
		defaults: {
			name: 'Formstack Trigger',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'formstackApi',
				required: true,
				displayOptions: {
					show: {
						authentication: ['accessToken'],
					},
				},
			},
			{
				name: 'formstackOAuth2Api',
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
						name: 'Access Token',
						value: 'accessToken',
					},
					{
						name: 'OAuth2',
						value: 'oAuth2',
					},
				],
				default: 'accessToken',
			},
			{
				displayName: 'Form Name or ID',
				name: 'formId',
				type: 'options',
				typeOptions: {
					loadOptionsMethod: 'getForms',
				},
				default: '',
				required: true,
				description:
					'The Formstack form to monitor for new submissions. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
			},
			{
				displayName: 'Simplify',
				name: 'simple',
				type: 'boolean',
				default: true,
				description:
					'Whether to return a simplified version of the response instead of the raw data',
			},
		],
	};

	methods = {
		loadOptions: {
			getForms,
		},
	};

	webhookMethods = {
		default: {
			async checkExists(this: IHookFunctions): Promise<boolean> {
				const webhookUrl = this.getNodeWebhookUrl('default');
				const webhookData = this.getWorkflowStaticData('node');

				const formId = this.getNodeParameter('formId') as string;

				const endpoint = `form/${formId}/webhook.json`;

				const { webhooks } = await apiRequest.call(this, 'GET', endpoint);

				for (const webhook of webhooks) {
					if (webhook.url === webhookUrl) {
						webhookData.webhookId = webhook.id;
						return true;
					}
				}

				return false;
			},
			async create(this: IHookFunctions): Promise<boolean> {
				const webhookUrl = this.getNodeWebhookUrl('default');

				const formId = this.getNodeParameter('formId') as string;

				const endpoint = `form/${formId}/webhook.json`;

				// TODO: Add handshake key support
				const body = {
					url: webhookUrl,
					standardize_field_values: true,
					include_field_type: true,
					content_type: 'json',
				};

				const response = await apiRequest.call(this, 'POST', endpoint, body);

				const webhookData = this.getWorkflowStaticData('node');
				webhookData.webhookId = response.id;
				return true;
			},
			async delete(this: IHookFunctions): Promise<boolean> {
				const webhookData = this.getWorkflowStaticData('node');

				if (webhookData.webhookId !== undefined) {
					const endpoint = `webhook/${webhookData.webhookId}.json`;

					try {
						const body = {};
						await apiRequest.call(this, 'DELETE', endpoint, body);
					} catch (e) {
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
		const bodyData = this.getBodyData() as unknown as IFormstackWebhookResponseBody;
		const simple = this.getNodeParameter('simple') as string;

		const response = bodyData as unknown as IDataObject;

		if (simple) {
			for (const key of Object.keys(response)) {
				if ((response[key] as IDataObject).hasOwnProperty('value')) {
					response[key] = (response[key] as IDataObject).value;
				}
			}
		}

		return {
			workflowData: [this.helpers.returnJsonArray([response as unknown as IDataObject])],
		};
	}
}
