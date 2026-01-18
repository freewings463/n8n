"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Merge/v3/actions/mode/combineAll.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Merge/v3 的节点。导入/依赖:外部:lodash/merge、@utils/utilities；内部:无；本地:../helpers/descriptions、../helpers/interfaces、../helpers/utils。导出:properties、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Merge/v3/actions/mode/combineAll.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Merge/v3/actions/mode/combineAll.py

import merge from 'lodash/merge';
import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
	IPairedItemData,
} from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { clashHandlingProperties, fuzzyCompareProperty } from '../../helpers/descriptions';
import type { ClashResolveOptions } from '../../helpers/interfaces';
import { addSuffixToEntriesKeys, selectMergeMethod } from '../../helpers/utils';

export const properties: INodeProperties[] = [
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [clashHandlingProperties, fuzzyCompareProperty],
	},
];

const displayOptions = {
	show: {
		mode: ['combine'],
		combineBy: ['combineAll'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	inputsData: INodeExecutionData[][],
): Promise<INodeExecutionData[][]> {
	const returnData: INodeExecutionData[] = [];

	const clashHandling = this.getNodeParameter(
		'options.clashHandling.values',
		0,
		{},
	) as ClashResolveOptions;

	let input1 = inputsData[0];
	let input2 = inputsData[1];

	if (clashHandling.resolveClash === 'preferInput1') {
		[input1, input2] = [input2, input1];
	}

	if (clashHandling.resolveClash === 'addSuffix') {
		input1 = addSuffixToEntriesKeys(input1, '1');
		input2 = addSuffixToEntriesKeys(input2, '2');
	}

	const mergeIntoSingleObject = selectMergeMethod(clashHandling);

	if (!input1 || !input2) {
		return [returnData];
	}

	let entry1: INodeExecutionData;
	let entry2: INodeExecutionData;

	for (entry1 of input1) {
		for (entry2 of input2) {
			returnData.push({
				json: {
					...mergeIntoSingleObject(entry1.json, entry2.json),
				},
				binary: {
					...merge({}, entry1.binary, entry2.binary),
				},
				pairedItem: [entry1.pairedItem as IPairedItemData, entry2.pairedItem as IPairedItemData],
			});
		}
	}

	return [returnData];
}
