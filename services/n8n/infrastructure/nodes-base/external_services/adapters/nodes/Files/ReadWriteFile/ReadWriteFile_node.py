"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Files/ReadWriteFile/ReadWriteFile.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Files/ReadWriteFile 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./actions/read.operation、./actions/write.operation。导出:ReadWriteFile。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Files/ReadWriteFile/ReadWriteFile.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Files/ReadWriteFile/ReadWriteFile_node.py

import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import * as read from './actions/read.operation';
import * as write from './actions/write.operation';

export class ReadWriteFile implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Read/Write Files from Disk',
		name: 'readWriteFile',
		icon: 'file:readWriteFile.svg',
		group: ['input'],
		version: [1, 1.1],
		description: 'Read or write files from the computer that runs n8n',
		defaults: {
			name: 'Read/Write Files from Disk',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName:
					'Use this node to read and write files on the same computer running n8n. To handle files between different computers please use other nodes (e.g. FTP, HTTP Request, AWS).',
				name: 'info',
				type: 'notice',
				default: '',
			},
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Read File(s) From Disk',
						value: 'read',
						description: 'Retrieve one or more files from the computer that runs n8n',
						action: 'Read File(s) From Disk',
					},
					{
						name: 'Write File to Disk',
						value: 'write',
						description: 'Create a binary file on the computer that runs n8n',
						action: 'Write File to Disk',
					},
				],
				default: 'read',
			},
			...read.description,
			...write.description,
		],
	};

	async execute(this: IExecuteFunctions) {
		const operation = this.getNodeParameter('operation', 0, 'read');
		const items = this.getInputData();
		let returnData: INodeExecutionData[] = [];

		if (operation === 'read') {
			returnData = await read.execute.call(this, items);
		}

		if (operation === 'write') {
			returnData = await write.execute.call(this, items);
		}

		return [returnData];
	}
}
