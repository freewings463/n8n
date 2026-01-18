"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Merge/v3/actions/mode/chooseBranch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Merge/v3 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../helpers/descriptions。导出:properties、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Merge/v3/actions/mode/chooseBranch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Merge/v3/actions/mode/chooseBranch.py

import { NodeOperationError } from 'n8n-workflow';
import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';

import { preparePairedItemDataArray, updateDisplayOptions } from '@utils/utilities';

import { numberInputsProperty } from '../../helpers/descriptions';

export const properties: INodeProperties[] = [
	numberInputsProperty,
	{
		displayName: 'Output Type',
		name: 'chooseBranchMode',
		type: 'options',
		options: [
			{
				name: 'Wait for All Inputs to Arrive',
				value: 'waitForAll',
			},
		],
		default: 'waitForAll',
	},
	{
		displayName: 'Output',
		name: 'output',
		type: 'options',
		options: [
			{
				name: 'Data of Specified Input',
				value: 'specifiedInput',
			},
			{
				name: 'A Single, Empty Item',
				value: 'empty',
			},
		],
		default: 'specifiedInput',
		displayOptions: {
			show: {
				chooseBranchMode: ['waitForAll'],
			},
		},
	},
	{
		// eslint-disable-next-line n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options
		displayName: 'Use Data of Input',
		name: 'useDataOfInput',
		type: 'options',
		default: 1,
		displayOptions: {
			show: {
				output: ['specifiedInput'],
			},
		},
		typeOptions: {
			minValue: 1,
			loadOptionsMethod: 'getInputs',
			loadOptionsDependsOn: ['numberInputs'],
		},
		// eslint-disable-next-line n8n-nodes-base/node-param-description-wrong-for-dynamic-options
		description: 'The number of the input to use data of',
		validateType: 'number',
	},
];

const displayOptions = {
	show: {
		mode: ['chooseBranch'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	inputsData: INodeExecutionData[][],
): Promise<INodeExecutionData[][]> {
	const returnData: INodeExecutionData[] = [];

	const chooseBranchMode = this.getNodeParameter('chooseBranchMode', 0) as string;

	if (chooseBranchMode === 'waitForAll') {
		const output = this.getNodeParameter('output', 0) as string;

		if (output === 'specifiedInput') {
			const useDataOfInput = this.getNodeParameter('useDataOfInput', 0) as number;
			if (useDataOfInput > inputsData.length) {
				throw new NodeOperationError(this.getNode(), `Input ${useDataOfInput} doesn't exist`, {
					description: `The node has only ${inputsData.length} inputs, so selecting input ${useDataOfInput} is not possible.`,
				});
			}

			const inputData = inputsData[useDataOfInput - 1];

			returnData.push.apply(returnData, inputData);
		}
		if (output === 'empty') {
			const pairedItem = [
				...this.getInputData(0).map((inputData) => inputData.pairedItem),
				...this.getInputData(1).map((inputData) => inputData.pairedItem),
			].flatMap(preparePairedItemDataArray);

			returnData.push({
				json: {},
				pairedItem,
			});
		}
	}

	return [returnData];
}
