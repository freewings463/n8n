"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/StopAndError/StopAndError.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/StopAndError 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./utils。导出:StopAndError。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/StopAndError/StopAndError.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/StopAndError/StopAndError_node.py

import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes, NodeOperationError } from 'n8n-workflow';

import { createErrorFromParameters } from './utils';

const errorObjectPlaceholder = `{
	"code": "404",
	"description": "The resource could not be fetched"
}`;

export class StopAndError implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Stop and Error',
		name: 'stopAndError',
		icon: 'fa:exclamation-triangle',
		iconColor: 'red',
		group: ['input'],
		version: 1,
		description: 'Throw an error in the workflow',
		defaults: {
			name: 'Stop and Error',
			color: '#ff0000',
		},
		inputs: [NodeConnectionTypes.Main],

		outputs: [],
		properties: [
			{
				displayName: 'Error Type',
				name: 'errorType',
				type: 'options',
				options: [
					{
						name: 'Error Message',
						value: 'errorMessage',
					},
					{
						name: 'Error Object',
						value: 'errorObject',
					},
				],
				default: 'errorMessage',
				description: 'Type of error to throw',
			},
			{
				displayName: 'Error Message',
				name: 'errorMessage',
				type: 'string',
				placeholder: 'An error occurred!',
				default: '',
				required: true,
				displayOptions: {
					show: {
						errorType: ['errorMessage'],
					},
				},
			},
			{
				displayName: 'Error Object',
				name: 'errorObject',
				type: 'json',
				description: 'Object containing error properties',
				default: '',
				typeOptions: {
					alwaysOpenEditWindow: true,
				},
				placeholder: errorObjectPlaceholder,
				required: true,
				displayOptions: {
					show: {
						errorType: ['errorObject'],
					},
				},
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const errorType = this.getNodeParameter('errorType', 0) as 'errorMessage' | 'errorObject';
		const errorParameter =
			errorType === 'errorMessage'
				? (this.getNodeParameter('errorMessage', 0) as string)
				: (this.getNodeParameter('errorObject', 0) as string);

		const { message, options } = createErrorFromParameters(errorType, errorParameter);

		throw new NodeOperationError(this.getNode(), message, options);
	}
}
