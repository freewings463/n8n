"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Adalo/Adalo.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Adalo 的节点。导入/依赖:外部:无；内部:无；本地:./CollectionDescription、./types。导出:Adalo。关键函数/方法:presendCreateUpdate。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Adalo/Adalo.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Adalo/Adalo_node.py

import {
	NodeConnectionTypes,
	type IDataObject,
	type IExecuteSingleFunctions,
	type IHttpRequestOptions,
	type INodeType,
	type INodeTypeDescription,
} from 'n8n-workflow';

import { collectionFields } from './CollectionDescription';
import type { FieldsUiValues } from './types';

export class Adalo implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Adalo',
		name: 'adalo',
		icon: 'file:adalo.svg',
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["collectionId"]}}',
		description: 'Consume Adalo API',
		defaults: {
			name: 'Adalo',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'adaloApi',
				required: true,
			},
		],
		requestDefaults: {
			baseURL: '=https://api.adalo.com/v0/apps/{{$credentials.appId}}',
		},
		requestOperations: {
			pagination: {
				type: 'offset',
				properties: {
					limitParameter: 'limit',
					offsetParameter: 'offset',
					pageSize: 100,
					type: 'query',
				},
			},
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				default: 'collection',
				options: [
					{
						name: 'Collection',
						value: 'collection',
					},
				],
			},
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Create',
						value: 'create',
						description: 'Create a row',
						routing: {
							send: {
								preSend: [this.presendCreateUpdate],
							},
							request: {
								method: 'POST',
								url: '=/collections/{{$parameter["collectionId"]}}',
							},
						},
						action: 'Create a row',
					},
					{
						name: 'Delete',
						value: 'delete',
						description: 'Delete a row',
						routing: {
							request: {
								method: 'DELETE',
								url: '=/collections/{{$parameter["collectionId"]}}/{{$parameter["rowId"]}}',
							},
							output: {
								postReceive: [
									{
										type: 'set',
										properties: {
											value: '={{ { "success": true } }}',
										},
									},
								],
							},
						},
						action: 'Delete a row',
					},
					{
						name: 'Get',
						value: 'get',
						description: 'Retrieve a row',
						routing: {
							request: {
								method: 'GET',
								url: '=/collections/{{$parameter["collectionId"]}}/{{$parameter["rowId"]}}',
							},
						},
						action: 'Retrieve a row',
					},
					{
						name: 'Get Many',
						value: 'getAll',
						description: 'Retrieve many rows',
						routing: {
							request: {
								method: 'GET',
								url: '=/collections/{{$parameter["collectionId"]}}',
								qs: {
									limit: '={{$parameter["limit"]}}',
								},
							},
							send: {
								paginate: '={{$parameter["returnAll"]}}',
							},
							output: {
								postReceive: [
									{
										type: 'rootProperty',
										properties: {
											property: 'records',
										},
									},
								],
							},
						},
						action: 'Retrieve all rows',
					},
					{
						name: 'Update',
						value: 'update',
						description: 'Update a row',
						routing: {
							send: {
								preSend: [this.presendCreateUpdate],
							},
							request: {
								method: 'PUT',
								url: '=/collections/{{$parameter["collectionId"]}}/{{$parameter["rowId"]}}',
							},
						},
						action: 'Update a row',
					},
				],
				default: 'getAll',
			},
			{
				displayName: 'Collection ID',
				name: 'collectionId',
				type: 'string',
				required: true,
				default: '',
				description:
					'Open your Adalo application and click on the three buttons beside the collection name, then select API Documentation',
				hint: "You can find information about app's collections on https://app.adalo.com/apps/<strong>your-app-id</strong>/api-docs",
				displayOptions: {
					show: {
						resource: ['collection'],
					},
				},
			},
			...collectionFields,
		],
	};

	async presendCreateUpdate(
		this: IExecuteSingleFunctions,
		requestOptions: IHttpRequestOptions,
	): Promise<IHttpRequestOptions> {
		const dataToSend = this.getNodeParameter('dataToSend', 0) as 'defineBelow' | 'autoMapInputData';

		requestOptions.body = {};

		if (dataToSend === 'autoMapInputData') {
			const inputData = this.getInputData();
			const rawInputsToIgnore = this.getNodeParameter('inputsToIgnore') as string;

			const inputKeysToIgnore = rawInputsToIgnore.split(',').map((c) => c.trim());
			const inputKeys = Object.keys(inputData.json).filter(
				(key) => !inputKeysToIgnore.includes(key),
			);

			for (const key of inputKeys) {
				(requestOptions.body as IDataObject)[key] = inputData.json[key];
			}
		} else {
			const fields = this.getNodeParameter('fieldsUi.fieldValues') as FieldsUiValues;

			for (const field of fields) {
				(requestOptions.body as IDataObject)[field.fieldId] = field.fieldValue;
			}
		}

		return requestOptions;
	}
}
