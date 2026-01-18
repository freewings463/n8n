"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ReadBinaryFile/ReadBinaryFile.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ReadBinaryFile 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:ReadBinaryFile。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ReadBinaryFile/ReadBinaryFile.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ReadBinaryFile/ReadBinaryFile_node.py

import {
	NodeConnectionTypes,
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeType,
	type INodeTypeDescription,
} from 'n8n-workflow';

export class ReadBinaryFile implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Read Binary File',
		name: 'readBinaryFile',
		icon: 'fa:file-import',
		group: ['input'],
		version: 1,
		hidden: true,
		description: 'Reads a binary file from disk',
		defaults: {
			name: 'Read Binary File',
			color: '#449922',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName: 'File Path',
				name: 'filePath',
				type: 'string',
				default: '',
				required: true,
				placeholder: '/data/example.jpg',
				description: 'Path of the file to read',
			},
			{
				displayName: 'Property Name',
				name: 'dataPropertyName',
				type: 'string',
				default: 'data',
				required: true,
				description: 'Name of the binary property to which to write the data of the read file',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();

		const returnData: INodeExecutionData[] = [];
		const length = items.length;
		let item: INodeExecutionData;

		for (let itemIndex = 0; itemIndex < length; itemIndex++) {
			try {
				item = items[itemIndex];
				const newItem: INodeExecutionData = {
					json: item.json,
					binary: {},
					pairedItem: {
						item: itemIndex,
					},
				};

				if (item.binary !== undefined && newItem.binary) {
					// Create a shallow copy of the binary data so that the old
					// data references which do not get changed still stay behind
					// but the incoming data does not get changed.
					Object.assign(newItem.binary, item.binary);
				}

				const filePath = this.getNodeParameter('filePath', itemIndex);

				const stream = await this.helpers.createReadStream(
					await this.helpers.resolvePath(filePath),
				);
				const dataPropertyName = this.getNodeParameter('dataPropertyName', itemIndex);

				newItem.binary![dataPropertyName] = await this.helpers.prepareBinaryData(stream, filePath);
				returnData.push(newItem);
			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({
						json: {
							error: (error as Error).message,
						},
						pairedItem: {
							item: itemIndex,
						},
					});
					continue;
				}
				throw error;
			}
		}

		return [returnData];
	}
}
