"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mindee/Mindee.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mindee 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:Mindee。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mindee/Mindee.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mindee/Mindee_node.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes, NodeOperationError } from 'n8n-workflow';

import { cleanData, cleanDataPreviousApiVersions, mindeeApiRequest } from './GenericFunctions';

export class Mindee implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Mindee',
		name: 'mindee',
		icon: 'file:mindee.svg',
		group: ['input'],
		version: [1, 2, 3],
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Consume Mindee API',
		defaults: {
			name: 'Mindee',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'mindeeReceiptApi',
				required: true,
				displayOptions: {
					show: {
						resource: ['receipt'],
					},
				},
			},
			{
				name: 'mindeeInvoiceApi',
				required: true,
				displayOptions: {
					show: {
						resource: ['invoice'],
					},
				},
			},
		],
		properties: [
			{
				displayName: 'API Version',
				name: 'apiVersion',
				type: 'options',
				isNodeSetting: true,
				displayOptions: {
					show: {
						'@version': [1],
					},
				},
				options: [
					{
						name: '1',
						value: 1,
					},
					{
						name: '3',
						value: 3,
					},
					{
						name: '4',
						value: 4,
					},
				],
				default: 1,
				description: 'Which Mindee API Version to use',
			},
			{
				displayName: 'API Version',
				name: 'apiVersion',
				type: 'options',
				isNodeSetting: true,
				displayOptions: {
					show: {
						'@version': [2],
					},
				},
				options: [
					{
						name: '1',
						value: 1,
					},
					{
						name: '3',
						value: 3,
					},
					{
						name: '4',
						value: 4,
					},
				],
				default: 3,
				description: 'Which Mindee API Version to use',
			},
			{
				displayName: 'API Version',
				name: 'apiVersion',
				type: 'options',
				isNodeSetting: true,
				displayOptions: {
					show: {
						'@version': [3],
					},
				},
				options: [
					{
						name: '1',
						value: 1,
					},
					{
						name: '3',
						value: 3,
					},
					{
						name: '4',
						value: 4,
					},
				],
				default: 4,
				description: 'Which Mindee API Version to use',
			},
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Invoice',
						value: 'invoice',
					},
					{
						name: 'Receipt',
						value: 'receipt',
					},
				],
				default: 'receipt',
			},
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Predict',
						value: 'predict',
					},
				],
				default: 'predict',
			},
			{
				displayName: 'Input Binary Field',
				name: 'binaryPropertyName',
				type: 'string',
				required: true,
				default: 'data',
				displayOptions: {
					show: {
						operation: ['predict'],
						resource: ['receipt', 'invoice'],
					},
				},
				hint: 'The name of the input binary field containing the file to be uploaded',
			},
			{
				displayName: 'RAW Data',
				name: 'rawData',
				type: 'boolean',
				default: false,
				description: 'Whether to return the data exactly in the way it got received from the API',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: IDataObject[] = [];
		const length = items.length;
		let responseData;
		const version = this.getNodeParameter('apiVersion', 0) as number;
		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);
		let endpoint;
		for (let i = 0; i < length; i++) {
			try {
				if (resource === 'receipt') {
					if (operation === 'predict') {
						const rawData = this.getNodeParameter('rawData', i);
						const binaryPropertyName = this.getNodeParameter('binaryPropertyName', i);

						const binaryData = this.helpers.assertBinaryData(i, binaryPropertyName);
						const dataBuffer = await this.helpers.getBinaryDataBuffer(i, binaryPropertyName);

						if (version === 1) {
							responseData = await mindeeApiRequest.call(
								this,
								'POST',
								'/expense_receipts/v2/predict',
								{},
								{},
								{
									formData: {
										file: {
											value: dataBuffer,
											options: {
												filename: binaryData.fileName,
											},
										},
									},
								},
							);
						} else if (version === 3) {
							endpoint = '/expense_receipts/v3/predict';
							responseData = await mindeeApiRequest.call(
								this,
								'POST',
								endpoint,
								{},
								{},
								{
									formData: {
										document: {
											value: dataBuffer,
											options: {
												filename: binaryData.fileName,
											},
										},
									},
								},
							);
						} else if (version === 4) {
							endpoint = '/expense_receipts/v4/predict';
							responseData = await mindeeApiRequest.call(
								this,
								'POST',
								endpoint,
								{},
								{},
								{
									formData: {
										document: {
											value: dataBuffer,
											options: {
												filename: binaryData.fileName,
											},
										},
									},
								},
							);
						}
						if (!rawData) {
							if (version === 1) {
								responseData = cleanDataPreviousApiVersions(
									responseData.predictions as IDataObject[],
								);
							} else if (version === 3 || version === 4) {
								responseData = cleanData(responseData.document as IDataObject);
							}
						}
					}
				}

				if (resource === 'invoice') {
					if (operation === 'predict') {
						const rawData = this.getNodeParameter('rawData', i);
						const binaryPropertyName = this.getNodeParameter('binaryPropertyName', i);

						const binaryData = this.helpers.assertBinaryData(i, binaryPropertyName);
						const dataBuffer = await this.helpers.getBinaryDataBuffer(i, binaryPropertyName);

						if (version === 1) {
							endpoint = '/invoices/v1/predict';
							responseData = await mindeeApiRequest.call(
								this,
								'POST',
								endpoint,
								{},
								{},
								{
									formData: {
										file: {
											value: dataBuffer,
											options: {
												filename: binaryData.fileName,
											},
										},
									},
								},
							);
						} else if (version === 3) {
							endpoint = '/invoices/v3/predict';
							responseData = await mindeeApiRequest.call(
								this,
								'POST',
								endpoint,
								{},
								{},
								{
									formData: {
										document: {
											value: dataBuffer,
											options: {
												filename: binaryData.fileName,
											},
										},
									},
								},
							);
						} else if (version === 4) {
							endpoint = '/invoices/v4/predict';
							responseData = await mindeeApiRequest.call(
								this,
								'POST',
								endpoint,
								{},
								{},
								{
									formData: {
										document: {
											value: dataBuffer,
											options: {
												filename: binaryData.fileName,
											},
										},
									},
								},
							);
						} else {
							throw new NodeOperationError(this.getNode(), 'Invalid API version');
						}
						if (!rawData) {
							if (version === 1) {
								responseData = cleanDataPreviousApiVersions(
									responseData.predictions as IDataObject[],
								);
							} else if (version === 3 || version === 4) {
								responseData = cleanData(responseData.document as IDataObject);
							}
						}
					}
				}
				if (Array.isArray(responseData)) {
					returnData.push.apply(returnData, responseData as IDataObject[]);
				} else if (responseData !== undefined) {
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
