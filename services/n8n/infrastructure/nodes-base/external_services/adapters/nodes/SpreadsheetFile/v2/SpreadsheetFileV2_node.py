"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SpreadsheetFile/v2/SpreadsheetFileV2.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SpreadsheetFile/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./fromFile.operation、./toFile.operation、../description。导出:SpreadsheetFileV2。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SpreadsheetFile/v2/SpreadsheetFileV2.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SpreadsheetFile/v2/SpreadsheetFileV2_node.py

import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeBaseDescription,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import * as fromFile from './fromFile.operation';
import * as toFile from './toFile.operation';
import { operationProperty } from '../description';

export class SpreadsheetFileV2 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			version: 2,
			defaults: {
				name: 'Spreadsheet File',
				color: '#2244FF',
			},
			inputs: [NodeConnectionTypes.Main],
			outputs: [NodeConnectionTypes.Main],
			properties: [operationProperty, ...fromFile.description, ...toFile.description],
		};
	}

	async execute(this: IExecuteFunctions) {
		const items = this.getInputData();
		const operation = this.getNodeParameter('operation', 0);
		let returnData: INodeExecutionData[] = [];

		if (operation === 'fromFile') {
			returnData = await fromFile.execute.call(this, items);
		}

		if (operation === 'toFile') {
			returnData = await toFile.execute.call(this, items);
		}

		return [returnData];
	}
}
