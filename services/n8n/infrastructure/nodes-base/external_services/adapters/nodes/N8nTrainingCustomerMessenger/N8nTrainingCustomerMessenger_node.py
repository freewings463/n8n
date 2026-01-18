"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/N8nTrainingCustomerMessenger/N8nTrainingCustomerMessenger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/N8nTrainingCustomerMessenger 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:N8nTrainingCustomerMessenger。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/N8nTrainingCustomerMessenger/N8nTrainingCustomerMessenger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/N8nTrainingCustomerMessenger/N8nTrainingCustomerMessenger_node.py

import {
	NodeConnectionTypes,
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeType,
	type INodeTypeDescription,
} from 'n8n-workflow';

export class N8nTrainingCustomerMessenger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Customer Messenger (n8n training)',
		name: 'n8nTrainingCustomerMessenger',
		icon: {
			light: 'file:n8nTrainingCustomerMessenger.svg',
			dark: 'file:n8nTrainingCustomerMessenger.dark.svg',
		},
		group: ['transform'],
		version: 1,
		description: 'Dummy node used for n8n training',
		defaults: {
			name: 'Customer Messenger (n8n training)',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName: 'Customer ID',
				name: 'customerId',
				type: 'string',
				required: true,
				default: '',
			},
			{
				displayName: 'Message',
				name: 'message',
				type: 'string',
				required: true,
				typeOptions: {
					rows: 4,
				},
				default: '',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];
		const length = items.length;
		let responseData;

		for (let i = 0; i < length; i++) {
			const customerId = this.getNodeParameter('customerId', i) as string;

			const message = this.getNodeParameter('message', i) as string;

			responseData = { output: `Sent message to customer ${customerId}:  ${message}` };
			const executionData = this.helpers.constructExecutionMetaData(
				this.helpers.returnJsonArray(responseData),
				{ itemData: { item: i } },
			);

			returnData.push(...executionData);
		}
		return [returnData];
	}
}
