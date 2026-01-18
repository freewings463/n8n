"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Webflow/V2/actions/Item/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Webflow/V2 的节点。导入/依赖:外部:无；内部:无；本地:../utils/utilities、../../GenericFunctions。导出:description。关键函数/方法:execute、wrapData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Webflow/V2/actions/Item/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Webflow/V2/actions/Item/create_operation.py

import type {
	IDataObject,
	INodeExecutionData,
	INodeProperties,
	IExecuteFunctions,
} from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '../../../../../utils/utilities';
import { webflowApiRequest } from '../../../GenericFunctions';

const properties: INodeProperties[] = [
	{
		displayName: 'Site Name or ID',
		name: 'siteId',
		type: 'options',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getSites',
		},
		default: '',
		description:
			'ID of the site containing the collection whose items to add to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Collection Name or ID',
		name: 'collectionId',
		type: 'options',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getCollections',
			loadOptionsDependsOn: ['siteId'],
		},
		default: '',
		description:
			'ID of the collection to add an item to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Live',
		name: 'live',
		type: 'boolean',
		required: true,
		default: false,
		description: 'Whether the item should be published on the live site',
	},
	{
		displayName: 'Fields',
		name: 'fieldsUi',
		placeholder: 'Add Field',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
		},
		default: {},
		options: [
			{
				displayName: 'Field',
				name: 'fieldValues',
				values: [
					{
						displayName: 'Field Name or ID',
						name: 'fieldId',
						type: 'options',
						typeOptions: {
							loadOptionsMethod: 'getFields',
							loadOptionsDependsOn: ['collectionId'],
						},
						default: '',
						description:
							'Field to set for the item to create. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
					},
					{
						displayName: 'Field Value',
						name: 'fieldValue',
						type: 'string',
						default: '',
						description: 'Value to set for the item to create',
					},
				],
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['item'],
		operation: ['create'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	items: INodeExecutionData[],
): Promise<INodeExecutionData[]> {
	const returnData: INodeExecutionData[] = [];
	let responseData;
	for (let i = 0; i < items.length; i++) {
		try {
			const collectionId = this.getNodeParameter('collectionId', i) as string;

			const uiFields = this.getNodeParameter('fieldsUi.fieldValues', i, []) as IDataObject[];

			const live = this.getNodeParameter('live', i) as boolean;

			const fieldData = {} as IDataObject;

			uiFields.forEach((data) => (fieldData[data.fieldId as string] = data.fieldValue));

			const body: IDataObject = {
				fieldData,
			};

			responseData = await webflowApiRequest.call(
				this,
				'POST',
				`/collections/${collectionId}/items${live ? '/live' : ''}`,
				body,
			);

			const executionData = this.helpers.constructExecutionMetaData(
				wrapData(responseData.body as IDataObject[]),
				{ itemData: { item: i } },
			);

			returnData.push(...executionData);
		} catch (error) {
			if (this.continueOnFail()) {
				returnData.push({ json: { message: error.message, error } });
				continue;
			}
			throw error;
		}
	}

	return returnData;
}
