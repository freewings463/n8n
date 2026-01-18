"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Contentful/Contentful.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Contentful 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./AssetDescription、./ContentTypeDescription、./EntryDescription、./GenericFunctions 等2项。导出:Contentful。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Contentful/Contentful.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Contentful/Contentful_node.py

import type {
	IExecuteFunctions,
	IDataObject,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import * as AssetDescription from './AssetDescription';
import * as ContentTypeDescription from './ContentTypeDescription';
import * as EntryDescription from './EntryDescription';
import { contentfulApiRequestAllItems, contentfulApiRequest } from './GenericFunctions';
import * as LocaleDescription from './LocaleDescription';
import * as SpaceDescription from './SpaceDescription';

export class Contentful implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Contentful',
		name: 'contentful',
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:contentful.png',
		group: ['input'],
		version: 1,
		description: 'Consume Contentful API',
		defaults: {
			name: 'Contentful',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'contentfulApi',
				required: true,
			},
		],
		properties: [
			{
				displayName: 'Source',
				name: 'source',
				type: 'options',
				default: 'deliveryApi',
				description: 'Pick where your data comes from, delivery or preview API',
				options: [
					{
						name: 'Delivery API',
						value: 'deliveryApi',
					},
					{
						name: 'Preview API',
						value: 'previewApi',
					},
				],
			},
			// Resources:
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					AssetDescription.resource,
					ContentTypeDescription.resource,
					EntryDescription.resource,
					LocaleDescription.resource,
					SpaceDescription.resource,
				],
				default: 'entry',
			},

			// Operations:
			...SpaceDescription.operations,
			...ContentTypeDescription.operations,
			...EntryDescription.operations,
			...AssetDescription.operations,
			...LocaleDescription.operations,

			// Resource specific fields:
			...SpaceDescription.fields,
			...ContentTypeDescription.fields,
			...EntryDescription.fields,
			...AssetDescription.fields,
			...LocaleDescription.fields,
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);
		let responseData;

		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];
		const qs: Record<string, string | number> = {};

		for (let i = 0; i < items.length; i++) {
			try {
				if (resource === 'space') {
					if (operation === 'get') {
						const credentials = await this.getCredentials('contentfulApi');

						responseData = await contentfulApiRequest.call(
							this,
							'GET',
							`/spaces/${credentials?.spaceId}`,
						);
					}
				}
				if (resource === 'contentType') {
					if (operation === 'get') {
						const credentials = await this.getCredentials('contentfulApi');

						const env = this.getNodeParameter('environmentId', 0) as string;

						const id = this.getNodeParameter('contentTypeId', 0) as string;

						const additionalFields = this.getNodeParameter('additionalFields', i);

						responseData = await contentfulApiRequest.call(
							this,
							'GET',
							`/spaces/${credentials?.spaceId}/environments/${env}/content_types/${id}`,
						);

						if (!additionalFields.rawData) {
							responseData = responseData.fields;
						}
					}
				}
				if (resource === 'entry') {
					if (operation === 'get') {
						const credentials = await this.getCredentials('contentfulApi');

						const env = this.getNodeParameter('environmentId', 0) as string;

						const id = this.getNodeParameter('entryId', 0) as string;

						const additionalFields = this.getNodeParameter('additionalFields', i);

						responseData = await contentfulApiRequest.call(
							this,
							'GET',
							`/spaces/${credentials?.spaceId}/environments/${env}/entries/${id}`,
							{},
							qs,
						);

						if (!additionalFields.rawData) {
							responseData = responseData.fields;
						}
					} else if (operation === 'getAll') {
						const credentials = await this.getCredentials('contentfulApi');

						const returnAll = this.getNodeParameter('returnAll', 0);

						const additionalFields = this.getNodeParameter('additionalFields', i);
						const rawData = additionalFields.rawData;
						additionalFields.rawData = undefined;

						const env = this.getNodeParameter('environmentId', i) as string;

						Object.assign(qs, additionalFields);

						if (qs.equal) {
							const [atribute, value] = (qs.equal as string).split('=');
							qs[atribute] = value;
							delete qs.equal;
						}

						if (qs.notEqual) {
							const [atribute, value] = (qs.notEqual as string).split('=');
							qs[atribute] = value;
							delete qs.notEqual;
						}

						if (qs.include) {
							const [atribute, value] = (qs.include as string).split('=');
							qs[atribute] = value;
							delete qs.include;
						}

						if (qs.exclude) {
							const [atribute, value] = (qs.exclude as string).split('=');
							qs[atribute] = value;
							delete qs.exclude;
						}

						if (returnAll) {
							responseData = await contentfulApiRequestAllItems.call(
								this,
								'items',
								'GET',
								`/spaces/${credentials?.spaceId}/environments/${env}/entries`,
								{},
								qs,
							);

							if (!rawData) {
								const assets: IDataObject[] = [];

								responseData.map((asset: any) => {
									assets.push(asset.fields as IDataObject);
								});
								responseData = assets;
							}
						} else {
							const limit = this.getNodeParameter('limit', 0);
							qs.limit = limit;
							responseData = await contentfulApiRequest.call(
								this,
								'GET',
								`/spaces/${credentials?.spaceId}/environments/${env}/entries`,
								{},
								qs,
							);
							responseData = responseData.items;

							if (!rawData) {
								const assets: IDataObject[] = [];

								responseData.map((asset: any) => {
									assets.push(asset.fields as IDataObject);
								});
								responseData = assets;
							}
						}
					}
				}
				if (resource === 'asset') {
					if (operation === 'get') {
						const credentials = await this.getCredentials('contentfulApi');

						const env = this.getNodeParameter('environmentId', 0) as string;

						const id = this.getNodeParameter('assetId', 0) as string;

						const additionalFields = this.getNodeParameter('additionalFields', i);

						responseData = await contentfulApiRequest.call(
							this,
							'GET',
							`/spaces/${credentials?.spaceId}/environments/${env}/assets/${id}`,
							{},
							qs,
						);

						if (!additionalFields.rawData) {
							responseData = responseData.fields;
						}
					} else if (operation === 'getAll') {
						const credentials = await this.getCredentials('contentfulApi');

						const returnAll = this.getNodeParameter('returnAll', 0);

						const additionalFields = this.getNodeParameter('additionalFields', i);
						const rawData = additionalFields.rawData;
						additionalFields.rawData = undefined;

						const env = this.getNodeParameter('environmentId', i) as string;

						Object.assign(qs, additionalFields);

						if (qs.equal) {
							const [atribute, value] = (qs.equal as string).split('=');
							qs[atribute] = value;
							delete qs.equal;
						}

						if (qs.notEqual) {
							const [atribute, value] = (qs.notEqual as string).split('=');
							qs[atribute] = value;
							delete qs.notEqual;
						}

						if (qs.include) {
							const [atribute, value] = (qs.include as string).split('=');
							qs[atribute] = value;
							delete qs.include;
						}

						if (qs.exclude) {
							const [atribute, value] = (qs.exclude as string).split('=');
							qs[atribute] = value;
							delete qs.exclude;
						}

						if (returnAll) {
							responseData = await contentfulApiRequestAllItems.call(
								this,
								'items',
								'GET',
								`/spaces/${credentials?.spaceId}/environments/${env}/assets`,
								{},
								qs,
							);

							if (!rawData) {
								const assets: IDataObject[] = [];

								responseData.map((asset: any) => {
									assets.push(asset.fields as IDataObject);
								});
								responseData = assets;
							}
						} else {
							const limit = this.getNodeParameter('limit', i);
							qs.limit = limit;
							responseData = await contentfulApiRequest.call(
								this,
								'GET',
								`/spaces/${credentials?.spaceId}/environments/${env}/assets`,
								{},
								qs,
							);
							responseData = responseData.items;

							if (!rawData) {
								const assets: IDataObject[] = [];

								responseData.map((asset: any) => {
									assets.push(asset.fields as IDataObject);
								});
								responseData = assets;
							}
						}
					}
				}
				if (resource === 'locale') {
					if (operation === 'getAll') {
						const credentials = await this.getCredentials('contentfulApi');

						const returnAll = this.getNodeParameter('returnAll', 0);

						const env = this.getNodeParameter('environmentId', i) as string;

						if (returnAll) {
							responseData = await contentfulApiRequestAllItems.call(
								this,
								'items',
								'GET',
								`/spaces/${credentials?.spaceId}/environments/${env}/locales`,
								{},
								qs,
							);
						} else {
							const limit = this.getNodeParameter('limit', 0);
							qs.limit = limit;
							responseData = await contentfulApiRequest.call(
								this,
								'GET',
								`/spaces/${credentials?.spaceId}/environments/${env}/locales`,
								{},
								qs,
							);
							responseData = responseData.items;
						}
					}
				}
				const executionData = this.helpers.constructExecutionMetaData(
					this.helpers.returnJsonArray(responseData as IDataObject[]),
					{ itemData: { item: i } },
				);
				returnData.push(...executionData);
			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({ error: error.message, json: {} });
					continue;
				}
				throw error;
			}
		}
		return [returnData];
	}
}
