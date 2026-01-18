"""
MIGRATION-META:
  source_path: packages/node-dev/templates/execute/simple.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/node-dev/templates/execute 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:ClassNameReplace。关键函数/方法:execute。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/node-dev/templates/execute/simple.ts -> services/n8n/infrastructure/node-dev/external_services/adapters/nodes/templates/execute/simple.py

import {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';

export class ClassNameReplace implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'DisplayNameReplace',
		name: 'N8nNameReplace',
		group: ['transform'],
		version: 1,
		description: 'NodeDescriptionReplace',
		defaults: {
			name: 'DisplayNameReplace',
			color: '#772244',
		},
		inputs: ['main'],
		outputs: ['main'],
		properties: [
			// Node properties which the user gets displayed and
			// can change on the node.
			{
				displayName: 'My String',
				name: 'myString',
				type: 'string',
				default: '',
				placeholder: 'Placeholder value',
				description: 'The description text',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();

		let item: INodeExecutionData;
		let myString: string;

		// Iterates over all input items and add the key "myString" with the
		// value the parameter "myString" resolves to.
		// (This could be a different value for each item in case it contains an expression)
		for (let itemIndex = 0; itemIndex < items.length; itemIndex++) {
			myString = this.getNodeParameter('myString', itemIndex, '') as string;
			item = items[itemIndex];

			item.json.myString = myString;
		}

		return [items];
	}
}
