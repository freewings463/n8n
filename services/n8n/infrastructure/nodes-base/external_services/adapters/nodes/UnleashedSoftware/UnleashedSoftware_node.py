"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/UnleashedSoftware/UnleashedSoftware.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/UnleashedSoftware 的节点。导入/依赖:外部:moment-timezone；内部:无；本地:./SalesOrderDescription、./StockOnHandDescription。导出:UnleashedSoftware。关键函数/方法:execute、convertNETDates。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/UnleashedSoftware/UnleashedSoftware.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/UnleashedSoftware/UnleashedSoftware_node.py

import moment from 'moment-timezone';
import {
	type IExecuteFunctions,
	type IDataObject,
	type INodeExecutionData,
	type INodeType,
	type INodeTypeDescription,
	NodeConnectionTypes,
} from 'n8n-workflow';

import {
	convertNETDates,
	unleashedApiRequest,
	unleashedApiRequestAllItems,
} from './GenericFunctions';
import { salesOrderFields, salesOrderOperations } from './SalesOrderDescription';
import { stockOnHandFields, stockOnHandOperations } from './StockOnHandDescription';

export class UnleashedSoftware implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Unleashed Software',
		name: 'unleashedSoftware',
		group: ['transform'],
		subtitle: '={{$parameter["operation"] + ":" + $parameter["resource"]}}',
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:unleashedSoftware.png',
		version: 1,
		description: 'Consume Unleashed Software API',
		defaults: {
			name: 'Unleashed Software',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'unleashedSoftwareApi',
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
						name: 'Sales Order',
						value: 'salesOrder',
					},
					{
						name: 'Stock On Hand',
						value: 'stockOnHand',
					},
				],
				default: 'salesOrder',
			},
			...salesOrderOperations,
			...salesOrderFields,

			...stockOnHandOperations,
			...stockOnHandFields,
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];
		const length = items.length;
		const qs: IDataObject = {};
		let responseData: IDataObject | IDataObject[] = [];

		for (let i = 0; i < length; i++) {
			const resource = this.getNodeParameter('resource', 0);
			const operation = this.getNodeParameter('operation', 0);

			//https://apidocs.unleashedsoftware.com/SalesOrders
			if (resource === 'salesOrder') {
				if (operation === 'getAll') {
					const returnAll = this.getNodeParameter('returnAll', i);
					const filters = this.getNodeParameter('filters', i);

					if (filters.startDate) {
						filters.startDate = moment(filters.startDate as string).format('YYYY-MM-DD');
					}

					if (filters.endDate) {
						filters.endDate = moment(filters.endDate as string).format('YYYY-MM-DD');
					}

					if (filters.modifiedSince) {
						filters.modifiedSince = moment(filters.modifiedSince as string).format('YYYY-MM-DD');
					}

					if (filters.orderStatus) {
						filters.orderStatus = (filters.orderStatus as string[]).join(',');
					}

					Object.assign(qs, filters);

					if (returnAll) {
						responseData = await unleashedApiRequestAllItems.call(
							this,
							'Items',
							'GET',
							'/SalesOrders',
							{},
							qs,
						);
					} else {
						const limit = this.getNodeParameter('limit', i);
						qs.pageSize = limit;
						responseData = (await unleashedApiRequest.call(
							this,
							'GET',
							'/SalesOrders',
							{},
							qs,
							1,
						)) as IDataObject;
						responseData = responseData.Items as IDataObject[];
					}
					convertNETDates(responseData);
					responseData = this.helpers.constructExecutionMetaData(
						this.helpers.returnJsonArray(responseData),
						{ itemData: { item: i } },
					);
				}
			}

			//https://apidocs.unleashedsoftware.com/StockOnHand
			if (resource === 'stockOnHand') {
				if (operation === 'getAll') {
					const returnAll = this.getNodeParameter('returnAll', i);

					const filters = this.getNodeParameter('filters', i);

					if (filters.asAtDate) {
						filters.asAtDate = moment(filters.asAtDate as string).format('YYYY-MM-DD');
					}

					if (filters.modifiedSince) {
						filters.modifiedSince = moment(filters.modifiedSince as string).format('YYYY-MM-DD');
					}

					if (filters.orderBy) {
						filters.orderBy = (filters.orderBy as string).trim();
					}

					Object.assign(qs, filters);

					if (returnAll) {
						responseData = await unleashedApiRequestAllItems.call(
							this,
							'Items',
							'GET',
							'/StockOnHand',
							{},
							qs,
						);
					} else {
						const limit = this.getNodeParameter('limit', i);
						qs.pageSize = limit;
						responseData = (await unleashedApiRequest.call(
							this,
							'GET',
							'/StockOnHand',
							{},
							qs,
							1,
						)) as IDataObject;
						responseData = responseData.Items as IDataObject[];
					}

					convertNETDates(responseData);
					responseData = this.helpers.constructExecutionMetaData(
						this.helpers.returnJsonArray(responseData),
						{ itemData: { item: i } },
					);
				}

				if (operation === 'get') {
					const productId = this.getNodeParameter('productId', i) as string;
					responseData = await unleashedApiRequest.call(this, 'GET', `/StockOnHand/${productId}`);
					convertNETDates(responseData);
				}
			}
			const executionData = this.helpers.constructExecutionMetaData(
				this.helpers.returnJsonArray(responseData),
				{ itemData: { item: i } },
			);
			returnData.push(...executionData);
		}

		return [returnData];
	}
}
