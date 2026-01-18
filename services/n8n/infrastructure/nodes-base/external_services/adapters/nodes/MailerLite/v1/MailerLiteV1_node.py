"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MailerLite/v1/MailerLiteV1.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MailerLite/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./SubscriberDescription。导出:MailerLiteV1。关键函数/方法:execute、customFieldsValues。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MailerLite/v1/MailerLiteV1.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MailerLite/v1/MailerLiteV1_node.py

import type {
	IExecuteFunctions,
	IDataObject,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	INodeTypeBaseDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { subscriberFields, subscriberOperations } from './SubscriberDescription';
import {
	getCustomFields,
	mailerliteApiRequest,
	mailerliteApiRequestAllItems,
} from '../GenericFunctions';

export class MailerLiteV1 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			displayName: 'MailerLite',
			name: 'mailerLite',
			group: ['input'],
			version: 1,
			subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
			description: 'Consume Mailer Lite API',
			defaults: {
				name: 'MailerLite',
			},
			inputs: [NodeConnectionTypes.Main],
			outputs: [NodeConnectionTypes.Main],
			credentials: [
				{
					name: 'mailerLiteApi',
					required: true,
				},
			],
			properties: [
				{
					displayName: 'Resource',
					name: 'resource',
					type: 'options',
					noDataExpression: true,
					options: [
						{
							name: 'Subscriber',
							value: 'subscriber',
						},
					],
					default: 'subscriber',
				},
				...subscriberOperations,
				...subscriberFields,
			],
		};
	}

	methods = {
		loadOptions: {
			getCustomFields,
		},
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];
		const length = items.length;
		const qs: IDataObject = {};
		let responseData;
		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);
		for (let i = 0; i < length; i++) {
			try {
				if (resource === 'subscriber') {
					//https://developers.mailerlite.com/reference#create-a-subscriber
					if (operation === 'create') {
						const email = this.getNodeParameter('email', i) as string;

						const additionalFields = this.getNodeParameter('additionalFields', i);

						const body: IDataObject = {
							email,
							fields: [],
						};

						Object.assign(body, additionalFields);

						if (additionalFields.customFieldsUi) {
							const customFieldsValues = (additionalFields.customFieldsUi as IDataObject)
								.customFieldsValues as IDataObject[];

							if (customFieldsValues) {
								const fields = {};

								for (const customFieldValue of customFieldsValues) {
									//@ts-ignore
									fields[customFieldValue.fieldId] = customFieldValue.value;
								}

								body.fields = fields;
								delete body.customFieldsUi;
							}
						}

						responseData = await mailerliteApiRequest.call(this, 'POST', '/subscribers', body);
					}
					//https://developers.mailerlite.com/reference#single-subscriber
					if (operation === 'get') {
						const subscriberId = this.getNodeParameter('subscriberId', i) as string;

						responseData = await mailerliteApiRequest.call(
							this,
							'GET',
							`/subscribers/${subscriberId}`,
						);
					}
					//https://developers.mailerlite.com/reference#subscribers
					if (operation === 'getAll') {
						const returnAll = this.getNodeParameter('returnAll', i);

						const filters = this.getNodeParameter('filters', i);

						Object.assign(qs, filters);

						if (returnAll) {
							responseData = await mailerliteApiRequestAllItems.call(
								this,
								'GET',
								'/subscribers',
								{},
								qs,
							);
						} else {
							qs.limit = this.getNodeParameter('limit', i);

							responseData = await mailerliteApiRequest.call(this, 'GET', '/subscribers', {}, qs);
						}
					}
					//https://developers.mailerlite.com/reference#update-subscriber
					if (operation === 'update') {
						const subscriberId = this.getNodeParameter('subscriberId', i) as string;

						const updateFields = this.getNodeParameter('updateFields', i);

						const body: IDataObject = {};

						Object.assign(body, updateFields);

						if (updateFields.customFieldsUi) {
							const customFieldsValues = (updateFields.customFieldsUi as IDataObject)
								.customFieldsValues as IDataObject[];

							if (customFieldsValues) {
								const fields = {};

								for (const customFieldValue of customFieldsValues) {
									//@ts-ignore
									fields[customFieldValue.fieldId] = customFieldValue.value;
								}

								body.fields = fields;
								delete body.customFieldsUi;
							}
						}

						responseData = await mailerliteApiRequest.call(
							this,
							'PUT',
							`/subscribers/${subscriberId}`,
							body,
						);
					}
				}
			} catch (error) {
				if (this.continueOnFail()) {
					const executionErrorData = this.helpers.constructExecutionMetaData(
						this.helpers.returnJsonArray({ error: error.message }),
						{ itemData: { item: i } },
					);
					returnData.push(...executionErrorData);
					continue;
				}
				throw error;
			}

			const executionData = this.helpers.constructExecutionMetaData(
				this.helpers.returnJsonArray(responseData as IDataObject[]),
				{ itemData: { item: i } },
			);

			returnData.push(...executionData);
		}

		return [returnData];
	}
}
