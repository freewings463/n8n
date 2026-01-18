"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/N8nTrainingCustomerDatastore/N8nTrainingCustomerDatastore.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/N8nTrainingCustomerDatastore 的Store。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:N8nTrainingCustomerDatastore。关键函数/方法:execute。用于管理该模块前端状态（state/actions/getters）供UI消费。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/N8nTrainingCustomerDatastore/N8nTrainingCustomerDatastore.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/N8nTrainingCustomerDatastore/N8nTrainingCustomerDatastore_node.py

import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

const data = [
	{
		id: '23423532',
		name: 'Jay Gatsby',
		email: 'gatsby@west-egg.com',
		notes: 'Keeps asking about a green light??',
		country: 'US',
		created: '1925-04-10',
	},
	{
		id: '23423533',
		name: 'José Arcadio Buendía',
		email: 'jab@macondo.co',
		notes: 'Lots of people named after him. Very confusing',
		country: 'CO',
		created: '1967-05-05',
	},
	{
		id: '23423534',
		name: 'Max Sendak',
		email: 'info@in-and-out-of-weeks.org',
		notes: 'Keeps rolling his terrible eyes',
		country: 'US',
		created: '1963-04-09',
	},
	{
		id: '23423535',
		name: 'Zaphod Beeblebrox',
		email: 'captain@heartofgold.com',
		notes: 'Felt like I was talking to more than one person',
		country: null,
		created: '1979-10-12',
	},
	{
		id: '23423536',
		name: 'Edmund Pevensie',
		email: 'edmund@narnia.gov',
		notes: 'Passionate sailor',
		country: 'UK',
		created: '1950-10-16',
	},
];

export class N8nTrainingCustomerDatastore implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Customer Datastore (n8n training)',
		name: 'n8nTrainingCustomerDatastore',
		icon: {
			light: 'file:n8nTrainingCustomerDatastore.svg',
			dark: 'file:n8nTrainingCustomerDatastore.dark.svg',
		},
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"]}}',
		description: 'Dummy node used for n8n training',
		defaults: {
			name: 'Customer Datastore (n8n training)',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Get One Person',
						value: 'getOnePerson',
					},
					{
						name: 'Get All People',
						value: 'getAllPeople',
					},
				],
				default: 'getOnePerson',
			},
			{
				displayName: 'Return All',
				name: 'returnAll',
				type: 'boolean',
				displayOptions: {
					show: {
						operation: ['getAllPeople'],
					},
				},
				default: false,
				description: 'Whether to return all results or only up to a given limit',
			},
			{
				displayName: 'Limit',
				name: 'limit',
				type: 'number',
				displayOptions: {
					show: {
						operation: ['getAllPeople'],
						returnAll: [false],
					},
				},
				typeOptions: {
					minValue: 1,
					maxValue: 10,
				},
				default: 5,
				description: 'Max number of results to return',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];
		const length = items.length;
		const operation = this.getNodeParameter('operation', 0);
		let responseData;

		for (let i = 0; i < length; i++) {
			if (operation === 'getOnePerson') {
				responseData = data[0];
			}

			if (operation === 'getAllPeople') {
				const returnAll = this.getNodeParameter('returnAll', i);

				if (returnAll) {
					responseData = data;
				} else {
					const limit = this.getNodeParameter('limit', i);
					responseData = data.slice(0, limit);
				}
			}

			if (Array.isArray(responseData)) {
				const executionData = this.helpers.constructExecutionMetaData(
					this.helpers.returnJsonArray(responseData),
					{ itemData: { item: i } },
				);
				returnData.push.apply(returnData, executionData);
			} else if (responseData !== undefined) {
				returnData.push({ json: responseData });
			}
		}
		return [returnData];
	}
}
