"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Bitly/Bitly.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Bitly 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions、./LinkDescription。导出:Bitly。关键函数/方法:execute、getGroups、getTags、deeplinks。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Bitly/Bitly.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Bitly/Bitly_node.py

import type {
	IExecuteFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	INodeExecutionData,
	INodePropertyOptions,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { bitlyApiRequest, bitlyApiRequestAllItems } from './GenericFunctions';
import { linkFields, linkOperations } from './LinkDescription';

export class Bitly implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Bitly',
		name: 'bitly',
		icon: 'file:bitly.svg',
		group: ['output'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Consume Bitly API',
		defaults: {
			name: 'Bitly',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'bitlyApi',
				required: true,
				displayOptions: {
					show: {
						authentication: ['accessToken'],
					},
				},
			},
			{
				name: 'bitlyOAuth2Api',
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
						name: 'Link',
						value: 'link',
					},
				],
				default: 'link',
			},
			...linkOperations,
			...linkFields,
		],
	};

	methods = {
		loadOptions: {
			// Get all the available groups to display them to user so that they can
			// select them easily
			async getGroups(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				const returnData: INodePropertyOptions[] = [];
				const groups = await bitlyApiRequestAllItems.call(this, 'groups', 'GET', '/groups');
				for (const group of groups) {
					const groupName = group.name;
					const groupId = group.guid;
					returnData.push({
						name: groupName,
						value: groupId,
					});
				}
				return returnData;
			},
			// Get all the available tags to display them to user so that they can
			// select them easily
			async getTags(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				const groupId = this.getCurrentNodeParameter('group') as string;
				const returnData: INodePropertyOptions[] = [];
				const tags = await bitlyApiRequestAllItems.call(
					this,
					'tags',
					'GET',
					`groups/${groupId}/tags`,
				);
				for (const tag of tags) {
					const tagName = tag;
					const tagId = tag;
					returnData.push({
						name: tagName,
						value: tagId,
					});
				}
				return returnData;
			},
		},
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];
		const length = items.length;
		let responseData;
		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);
		for (let i = 0; i < length; i++) {
			try {
				if (resource === 'link') {
					if (operation === 'create') {
						const longUrl = this.getNodeParameter('longUrl', i) as string;
						const additionalFields = this.getNodeParameter('additionalFields', i);
						const body: IDataObject = {
							long_url: longUrl,
						};
						if (additionalFields.title) {
							body.title = additionalFields.title as string;
						}
						if (additionalFields.domain) {
							body.domain = additionalFields.domain as string;
						}
						if (additionalFields.group) {
							body.group = additionalFields.group as string;
						}
						if (additionalFields.tags) {
							body.tags = additionalFields.tags as string[];
						}
						const deeplinks = (this.getNodeParameter('deeplink', i) as IDataObject)
							.deeplinkUi as IDataObject[];
						if (deeplinks) {
							for (const deeplink of deeplinks) {
								//@ts-ignore
								body.deeplinks.push({
									app_uri_path: deeplink.appUriPath,
									install_type: deeplink.installType,
									install_url: deeplink.installUrl,
									app_id: deeplink.appId,
								});
							}
						}
						responseData = await bitlyApiRequest.call(this, 'POST', '/bitlinks', body);
					}
					if (operation === 'update') {
						const linkId = this.getNodeParameter('id', i) as string;
						const updateFields = this.getNodeParameter('updateFields', i);
						const body: IDataObject = {};
						if (updateFields.longUrl) {
							body.long_url = updateFields.longUrl as string;
						}
						if (updateFields.title) {
							body.title = updateFields.title as string;
						}
						if (updateFields.archived !== undefined) {
							body.archived = updateFields.archived as boolean;
						}
						if (updateFields.group) {
							body.group = updateFields.group as string;
						}
						if (updateFields.tags) {
							body.tags = updateFields.tags as string[];
						}
						const deeplinks = (this.getNodeParameter('deeplink', i) as IDataObject)
							.deeplinkUi as IDataObject[];
						if (deeplinks) {
							for (const deeplink of deeplinks) {
								//@ts-ignore
								body.deeplinks.push({
									app_uri_path: deeplink.appUriPath,
									install_type: deeplink.installType,
									install_url: deeplink.installUrl,
									app_id: deeplink.appId,
								});
							}
						}
						responseData = await bitlyApiRequest.call(this, 'PATCH', `/bitlinks/${linkId}`, body);
					}
					if (operation === 'get') {
						const linkId = this.getNodeParameter('id', i) as string;
						responseData = await bitlyApiRequest.call(this, 'GET', `/bitlinks/${linkId}`);
					}
				}

				const executionData = this.helpers.constructExecutionMetaData(
					this.helpers.returnJsonArray(responseData as IDataObject[]),
					{ itemData: { item: i } },
				);
				returnData.push(...executionData);
			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({ error: error.message, json: {}, itemIndex: i });
					continue;
				}
				throw error;
			}
		}
		return [returnData];
	}
}
