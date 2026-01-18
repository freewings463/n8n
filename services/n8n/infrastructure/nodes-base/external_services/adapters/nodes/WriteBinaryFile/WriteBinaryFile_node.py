"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/WriteBinaryFile/WriteBinaryFile.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/WriteBinaryFile 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:WriteBinaryFile。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/WriteBinaryFile/WriteBinaryFile.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/WriteBinaryFile/WriteBinaryFile_node.py

import { BINARY_ENCODING, NodeConnectionTypes } from 'n8n-workflow';
import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { constants } from 'node:fs';
import type { Readable } from 'stream';

export class WriteBinaryFile implements INodeType {
	description: INodeTypeDescription = {
		hidden: true,
		displayName: 'Write Binary File',
		name: 'writeBinaryFile',
		icon: 'fa:file-export',
		group: ['output'],
		version: 1,
		description: 'Writes a binary file to disk',
		defaults: {
			name: 'Write Binary File',
			color: '#CC2233',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName: 'File Name',
				name: 'fileName',
				type: 'string',
				default: '',
				required: true,
				placeholder: '/data/example.jpg',
				description: 'Path to which the file should be written',
			},
			{
				displayName: 'Property Name',
				name: 'dataPropertyName',
				type: 'string',
				default: 'data',
				required: true,
				description:
					'Name of the binary property which contains the data for the file to be written',
			},
			{
				displayName: 'Options',
				name: 'options',
				type: 'collection',
				placeholder: 'Add option',
				default: {},
				options: [
					{
						displayName: 'Append',
						name: 'append',
						type: 'boolean',
						default: false,
						description: 'Whether to append to an existing file',
					},
				],
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
				const dataPropertyName = this.getNodeParameter('dataPropertyName', itemIndex);

				const fileName = this.getNodeParameter('fileName', itemIndex) as string;

				const options = this.getNodeParameter('options', 0, {});

				const flag: number = options.append
					? constants.O_APPEND
					: constants.O_WRONLY | constants.O_CREAT | constants.O_TRUNC;

				item = items[itemIndex];

				const newItem: INodeExecutionData = {
					json: {},
					pairedItem: {
						item: itemIndex,
					},
				};
				Object.assign(newItem.json, item.json);

				const binaryData = this.helpers.assertBinaryData(itemIndex, dataPropertyName);

				let fileContent: Buffer | Readable;
				if (binaryData.id) {
					fileContent = await this.helpers.getBinaryStream(binaryData.id);
				} else {
					fileContent = Buffer.from(binaryData.data, BINARY_ENCODING);
				}

				// Write the file to disk

				await this.helpers.writeContentToFile(
					await this.helpers.resolvePath(fileName),
					fileContent,
					flag,
				);

				if (item.binary !== undefined) {
					// Create a shallow copy of the binary data so that the old
					// data references which do not get changed still stay behind
					// but the incoming data does not get changed.
					newItem.binary = {};
					Object.assign(newItem.binary, item.binary);
				}

				// Add the file name to data

				newItem.json.fileName = fileName;

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
