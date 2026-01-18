"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Simulate/Simulate.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Simulate 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./methods。导出:Simulate。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Simulate/Simulate.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Simulate/Simulate_node.py

import { sleep, jsonParse, NodeOperationError, NodeConnectionTypes } from 'n8n-workflow';
import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	IDataObject,
} from 'n8n-workflow';

import {
	executionDurationProperty,
	iconSelector,
	jsonOutputProperty,
	subtitleProperty,
} from './descriptions';
import { loadOptions } from './methods';

export class Simulate implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Simulate',
		hidden: true,
		name: 'simulate',
		group: ['organization'],
		version: 1,
		description: 'Simulate a node',
		subtitle: '={{$parameter.subtitle || undefined}}',
		icon: 'fa:arrow-right',
		defaults: {
			name: 'Simulate',
			color: '#b0b0b0',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			iconSelector,
			subtitleProperty,
			{
				displayName: 'Output',
				name: 'output',
				type: 'options',
				default: 'all',
				noDataExpression: true,
				options: [
					{
						// eslint-disable-next-line n8n-nodes-base/node-param-display-name-miscased
						name: 'Returns all input items',
						value: 'all',
					},
					{
						// eslint-disable-next-line n8n-nodes-base/node-param-display-name-miscased
						name: 'Specify how many of input items to return',
						value: 'specify',
					},
					{
						// eslint-disable-next-line n8n-nodes-base/node-param-display-name-miscased
						name: 'Specify output as JSON',
						value: 'custom',
					},
				],
			},
			{
				displayName: 'Number of Items',
				name: 'numberOfItems',
				type: 'number',
				default: 1,
				description:
					'Number input of items to return, if greater then input length all items will be returned',
				displayOptions: {
					show: {
						output: ['specify'],
					},
				},
				typeOptions: {
					minValue: 1,
				},
			},
			{
				...jsonOutputProperty,
				displayOptions: {
					show: {
						output: ['custom'],
					},
				},
			},
			executionDurationProperty,
		],
	};

	methods = { loadOptions };

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		let returnItems: INodeExecutionData[] = [];

		const output = this.getNodeParameter('output', 0) as string;

		if (output === 'all') {
			returnItems = items;
		} else if (output === 'specify') {
			const numberOfItems = this.getNodeParameter('numberOfItems', 0) as number;

			returnItems = items.slice(0, numberOfItems);
		} else if (output === 'custom') {
			let jsonOutput = this.getNodeParameter('jsonOutput', 0);

			if (typeof jsonOutput === 'string') {
				try {
					jsonOutput = jsonParse<IDataObject>(jsonOutput);
				} catch (error) {
					throw new NodeOperationError(this.getNode(), 'Invalid JSON');
				}
			}

			if (!Array.isArray(jsonOutput)) {
				jsonOutput = [jsonOutput];
			}

			for (const item of jsonOutput as IDataObject[]) {
				returnItems.push({ json: item });
			}
		}

		const executionDuration = this.getNodeParameter('executionDuration', 0) as number;

		if (executionDuration > 0) {
			await sleep(executionDuration);
		}

		return [returnItems];
	}
}
