"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ReadBinaryFiles/ReadBinaryFiles.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ReadBinaryFiles 的节点。导入/依赖:外部:fast-glob；内部:无；本地:../utils/utilities。导出:ReadBinaryFiles。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ReadBinaryFiles/ReadBinaryFiles.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ReadBinaryFiles/ReadBinaryFiles_node.py

import glob from 'fast-glob';
import {
	NodeConnectionTypes,
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeType,
	type INodeTypeDescription,
} from 'n8n-workflow';

import { generatePairedItemData } from '../../utils/utilities';

export class ReadBinaryFiles implements INodeType {
	description: INodeTypeDescription = {
		hidden: true,
		displayName: 'Read Binary Files',
		name: 'readBinaryFiles',
		icon: 'fa:file-import',
		group: ['input'],
		version: 1,
		description: 'Reads binary files from disk',
		defaults: {
			name: 'Read Binary Files',
			color: '#44AA44',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName: 'File Selector',
				name: 'fileSelector',
				type: 'string',
				default: '',
				required: true,
				placeholder: '*.jpg',
				description: 'Pattern for files to read',
			},
			{
				displayName: 'Property Name',
				name: 'dataPropertyName',
				type: 'string',
				default: 'data',
				required: true,
				description: 'Name of the binary property to which to write the data of the read files',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const fileSelector = this.getNodeParameter('fileSelector', 0) as string;
		const dataPropertyName = this.getNodeParameter('dataPropertyName', 0);
		const pairedItem = generatePairedItemData(this.getInputData().length);

		const files = await glob(fileSelector);

		const items: INodeExecutionData[] = [];
		for (const filePath of files) {
			const stream = await this.helpers.createReadStream(await this.helpers.resolvePath(filePath));
			items.push({
				binary: {
					[dataPropertyName]: await this.helpers.prepareBinaryData(stream, filePath),
				},
				json: {},
				pairedItem,
			});
		}

		return [items];
	}
}
