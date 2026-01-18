"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Oura/Oura.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Oura 的节点。导入/依赖:外部:moment-timezone；内部:n8n-workflow；本地:./GenericFunctions、./ProfileDescription、./SummaryDescription。导出:Oura。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Oura/Oura.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Oura/Oura_node.py

import moment from 'moment-timezone';
import type {
	IExecuteFunctions,
	IDataObject,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { ouraApiRequest } from './GenericFunctions';
import { profileOperations } from './ProfileDescription';
import { summaryFields, summaryOperations } from './SummaryDescription';

export class Oura implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Oura',
		name: 'oura',
		icon: { light: 'file:oura.svg', dark: 'file:oura.dark.svg' },
		group: ['output'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Consume Oura API',
		defaults: {
			name: 'Oura',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'ouraApi',
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
						name: 'Profile',
						value: 'profile',
					},
					{
						name: 'Summary',
						value: 'summary',
					},
				],
				default: 'summary',
			},
			...profileOperations,
			...summaryOperations,
			...summaryFields,
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const length = items.length;

		let responseData;
		const returnData: INodeExecutionData[] = [];

		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);

		for (let i = 0; i < length; i++) {
			try {
				if (resource === 'profile') {
					// *********************************************************************
					//                             profile
					// *********************************************************************

					// https://cloud.ouraring.com/docs/personal-info

					if (operation === 'get') {
						// ----------------------------------
						//         profile: get
						// ----------------------------------

						responseData = await ouraApiRequest.call(this, 'GET', '/usercollection/personal_info');
					}
				} else if (resource === 'summary') {
					// *********************************************************************
					//                             summary
					// *********************************************************************

					// https://cloud.ouraring.com/docs/daily-summaries

					const qs: IDataObject = {};

					const { start, end } = this.getNodeParameter('filters', i) as {
						start: string;
						end: string;
					};

					const returnAll = this.getNodeParameter('returnAll', 0);

					if (start) {
						qs.start_date = moment(start).format('YYYY-MM-DD');
					}

					if (end) {
						qs.end_date = moment(end).format('YYYY-MM-DD');
					}

					if (operation === 'getActivity') {
						// ----------------------------------
						//       profile: getActivity
						// ----------------------------------

						responseData = await ouraApiRequest.call(
							this,
							'GET',
							'/usercollection/daily_activity',
							{},
							qs,
						);
						responseData = responseData.data;

						if (!returnAll) {
							const limit = this.getNodeParameter('limit', 0);
							responseData = responseData.splice(0, limit);
						}
					} else if (operation === 'getReadiness') {
						// ----------------------------------
						//       profile: getReadiness
						// ----------------------------------

						responseData = await ouraApiRequest.call(
							this,
							'GET',
							'/usercollection/daily_readiness',
							{},
							qs,
						);
						responseData = responseData.data;

						if (!returnAll) {
							const limit = this.getNodeParameter('limit', 0);
							responseData = responseData.splice(0, limit);
						}
					} else if (operation === 'getSleep') {
						// ----------------------------------
						//         profile: getSleep
						// ----------------------------------

						responseData = await ouraApiRequest.call(
							this,
							'GET',
							'/usercollection/daily_sleep',
							{},
							qs,
						);
						responseData = responseData.data;

						if (!returnAll) {
							const limit = this.getNodeParameter('limit', 0);
							responseData = responseData.splice(0, limit);
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
					const executionErrorData = this.helpers.constructExecutionMetaData(
						this.helpers.returnJsonArray({ error: error.message }),
						{ itemData: { item: i } },
					);
					returnData.push(...executionErrorData);
					continue;
				}
				throw error;
			}
		}
		return [returnData];
	}
}
