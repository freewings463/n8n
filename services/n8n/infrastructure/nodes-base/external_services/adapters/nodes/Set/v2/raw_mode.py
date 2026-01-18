"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Set/v2/raw.mode.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Set/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./helpers/interfaces、./helpers/utils、../utils/utilities。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Set/v2/raw.mode.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Set/v2/raw_mode.py

import type {
	INodeExecutionData,
	IExecuteFunctions,
	INodeProperties,
	IDataObject,
	INode,
} from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import type { SetNodeOptions } from './helpers/interfaces';
import { parseJsonParameter, composeReturnItem, resolveRawData } from './helpers/utils';
import { updateDisplayOptions } from '../../../utils/utilities';

const properties: INodeProperties[] = [
	{
		displayName: 'JSON',
		name: 'jsonOutput',
		type: 'json',
		typeOptions: {
			rows: 5,
		},
		default: '{\n  "my_field_1": "value",\n  "my_field_2": 1\n}\n',
		validateType: 'object',
		ignoreValidationDuringExecution: true,
	},
];

const displayOptions = {
	show: {
		mode: ['raw'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	item: INodeExecutionData,
	i: number,
	options: SetNodeOptions,
	rawData: IDataObject,
	node: INode,
) {
	try {
		let newData: IDataObject;
		if (rawData.jsonOutput === undefined) {
			const json = this.getNodeParameter('jsonOutput', i) as string;
			newData = parseJsonParameter(json, node, i);
		} else {
			newData = parseJsonParameter(
				resolveRawData.call(this, rawData.jsonOutput as string, i),
				node,
				i,
			);
		}

		return composeReturnItem.call(this, i, item, newData, options, node.typeVersion);
	} catch (error) {
		if (this.continueOnFail()) {
			return { json: { error: (error as Error).message }, pairedItem: { item: i } };
		}
		throw new NodeOperationError(node, error as Error, {
			itemIndex: i,
			description: error.description,
		});
	}
}
