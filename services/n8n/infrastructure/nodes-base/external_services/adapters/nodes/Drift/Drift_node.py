"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Drift/Drift.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Drift 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./ContactDescription、./ContactInterface、./GenericFunctions。导出:Drift。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Drift/Drift.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Drift/Drift_node.py

import type {
	IExecuteFunctions,
	IDataObject,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { contactFields, contactOperations } from './ContactDescription';
import type { IContact } from './ContactInterface';
import { driftApiRequest } from './GenericFunctions';

export class Drift implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Drift',
		name: 'drift',

		icon: { light: 'file:drift.svg', dark: 'file:drift.dark.svg' },
		group: ['output'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Consume Drift API',
		defaults: {
			name: 'Drift',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'driftApi',
				required: true,
				displayOptions: {
					show: {
						authentication: ['accessToken'],
					},
				},
			},
			{
				name: 'driftOAuth2Api',
				required: true,
				displayOptions: {
					show: {
						authentication: ['oAuth2'],
					},
				},
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
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Contact',
						value: 'contact',
					},
				],
				default: 'contact',
			},
			...contactOperations,
			...contactFields,
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: IDataObject[] = [];
		const length = items.length;
		let responseData;
		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);
		for (let i = 0; i < length; i++) {
			try {
				if (resource === 'contact') {
					//https://devdocs.drift.com/docs/creating-a-contact
					if (operation === 'create') {
						const email = this.getNodeParameter('email', i) as string;
						const additionalFields = this.getNodeParameter('additionalFields', i);
						const body: IContact = {
							email,
						};
						if (additionalFields.name) {
							body.name = additionalFields.name as string;
						}
						if (additionalFields.phone) {
							body.phone = additionalFields.phone as string;
						}
						responseData = await driftApiRequest.call(this, 'POST', '/contacts', {
							attributes: body,
						});
						responseData = responseData.data;
					}
					//https://devdocs.drift.com/docs/updating-a-contact
					if (operation === 'update') {
						const contactId = this.getNodeParameter('contactId', i) as string;
						const updateFields = this.getNodeParameter('updateFields', i);
						const body: IContact = {};
						if (updateFields.name) {
							body.name = updateFields.name as string;
						}
						if (updateFields.phone) {
							body.phone = updateFields.phone as string;
						}
						if (updateFields.email) {
							body.email = updateFields.email as string;
						}
						responseData = await driftApiRequest.call(this, 'PATCH', `/contacts/${contactId}`, {
							attributes: body,
						});
						responseData = responseData.data;
					}
					//https://devdocs.drift.com/docs/retrieving-contact
					if (operation === 'get') {
						const contactId = this.getNodeParameter('contactId', i) as string;
						responseData = await driftApiRequest.call(this, 'GET', `/contacts/${contactId}`);
						responseData = responseData.data;
					}
					//https://devdocs.drift.com/docs/listing-custom-attributes
					if (operation === 'getCustomAttributes') {
						responseData = await driftApiRequest.call(this, 'GET', '/contacts/attributes');
						responseData = responseData.data.properties;
					}
					//https://devdocs.drift.com/docs/removing-a-contact
					if (operation === 'delete') {
						const contactId = this.getNodeParameter('contactId', i) as string;
						responseData = await driftApiRequest.call(this, 'DELETE', `/contacts/${contactId}`);
						responseData = { success: true };
					}
				}
				if (Array.isArray(responseData)) {
					returnData.push.apply(returnData, responseData as IDataObject[]);
				} else {
					returnData.push(responseData as IDataObject);
				}
			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({ error: error.message });
					continue;
				}
				throw error;
			}
		}
		return [this.helpers.returnJsonArray(returnData)];
	}
}
