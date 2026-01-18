"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Cockpit/Cockpit.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Cockpit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./CollectionDescription、./FormDescription、./FormFunctions、./GenericFunctions 等2项。导出:Cockpit。关键函数/方法:execute、getCollections、getSingletons。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Cockpit/Cockpit.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Cockpit/Cockpit_node.py

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

import { collectionFields, collectionOperations } from './CollectionDescription';
import {
	createCollectionEntry,
	getAllCollectionEntries,
	getAllCollectionNames,
} from './CollectionFunctions';
import { formFields, formOperations } from './FormDescription';
import { submitForm } from './FormFunctions';
import { createDataFromParameters } from './GenericFunctions';
import { singletonFields, singletonOperations } from './SingletonDescription';
import { getAllSingletonNames, getSingleton } from './SingletonFunctions';

export class Cockpit implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Cockpit',
		name: 'cockpit',
		icon: { light: 'file:cockpit.svg', dark: 'file:cockpit.dark.svg' },
		group: ['output'],
		version: 1,
		subtitle: '={{ $parameter["operation"] + ": " + $parameter["resource"] }}',
		description: 'Consume Cockpit API',
		defaults: {
			name: 'Cockpit',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'cockpitApi',
				required: true,
			},
		],
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
					{
						name: 'Form',
						value: 'form',
					},
					{
						name: 'Singleton',
						value: 'singleton',
					},
				],
			},

			...collectionOperations,
			...collectionFields,
			...formOperations,
			...formFields,
			...singletonOperations,
			...singletonFields,
		],
	};

	methods = {
		loadOptions: {
			async getCollections(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				const collections = await getAllCollectionNames.call(this);

				return collections.map((itemName) => {
					return {
						name: itemName,
						value: itemName,
					};
				});
			},

			async getSingletons(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				const singletons = await getAllSingletonNames.call(this);

				return singletons.map((itemName) => {
					return {
						name: itemName,
						value: itemName,
					};
				});
			},
		},
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: IDataObject[] = [];
		const length = items.length;
		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);

		let responseData;

		for (let i = 0; i < length; i++) {
			try {
				if (resource === 'collection') {
					const collectionName = this.getNodeParameter('collection', i) as string;

					if (operation === 'create') {
						const data = createDataFromParameters.call(this, i);

						responseData = await createCollectionEntry.call(this, collectionName, data);
					} else if (operation === 'getAll') {
						const options = this.getNodeParameter('options', i);
						const returnAll = this.getNodeParameter('returnAll', i);

						if (!returnAll) {
							options.limit = this.getNodeParameter('limit', i);
						}

						responseData = await getAllCollectionEntries.call(this, collectionName, options);
					} else if (operation === 'update') {
						const id = this.getNodeParameter('id', i) as string;
						const data = createDataFromParameters.call(this, i);

						responseData = await createCollectionEntry.call(this, collectionName, data, id);
					}
				} else if (resource === 'form') {
					const formName = this.getNodeParameter('form', i) as string;

					if (operation === 'submit') {
						const form = createDataFromParameters.call(this, i);

						responseData = await submitForm.call(this, formName, form);
					}
				} else if (resource === 'singleton') {
					const singletonName = this.getNodeParameter('singleton', i) as string;

					if (operation === 'get') {
						responseData = await getSingleton.call(this, singletonName);
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
