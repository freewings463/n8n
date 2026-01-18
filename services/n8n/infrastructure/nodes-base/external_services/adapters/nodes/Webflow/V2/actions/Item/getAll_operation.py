"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Webflow/V2/actions/Item/getAll.operation.ts
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
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Webflow/V2/actions/Item/getAll.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Webflow/V2/actions/Item/getAll_operation.py

import type {
	IDataObject,
	INodeExecutionData,
	INodeProperties,
	IExecuteFunctions,
} from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '../../../../../utils/utilities';
import { webflowApiRequest, webflowApiRequestAllItems } from '../../../GenericFunctions';

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
			'ID of the site containing the collection whose items to operate on. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
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
			'ID of the collection whose items to operate on. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		displayOptions: {
			show: {
				returnAll: [false],
			},
		},
		default: 100,
		description: 'Max number of results to return',
	},
];

const displayOptions = {
	show: {
		resource: ['item'],
		operation: ['getAll'],
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
			const returnAll = this.getNodeParameter('returnAll', i);
			const collectionId = this.getNodeParameter('collectionId', i) as string;
			const qs: IDataObject = {};

			if (returnAll) {
				responseData = await webflowApiRequestAllItems.call(
					this,
					'GET',
					`/collections/${collectionId}/items`,
					{},
				);
			} else {
				qs.limit = this.getNodeParameter('limit', i);
				responseData = await webflowApiRequest.call(
					this,
					'GET',
					`/collections/${collectionId}/items`,
					{},
					qs,
				);
				responseData = responseData.body.items;
			}

			const executionData = this.helpers.constructExecutionMetaData(
				wrapData(responseData as IDataObject[]),
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
