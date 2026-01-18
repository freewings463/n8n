"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/StickyNote/StickyNote.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/StickyNote 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:StickyNote。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/StickyNote/StickyNote.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/StickyNote/StickyNote_node.py

import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';

export class StickyNote implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Sticky Note',
		name: 'stickyNote',
		icon: 'fa:sticky-note',
		group: ['input'],
		version: 1,
		description: 'Make your workflow easier to understand',
		defaults: {
			name: 'Sticky Note',
			color: '#FFD233',
		},

		inputs: [],

		outputs: [],
		properties: [
			{
				displayName: 'Content',
				name: 'content',
				type: 'string',
				default:
					"## I'm a note \n**Double click** to edit me. [Guide](https://docs.n8n.io/workflows/components/sticky-notes/)",
			},
			{
				displayName: 'Height',
				name: 'height',
				type: 'number',
				required: true,
				default: 160,
			},
			{
				displayName: 'Width',
				name: 'width',
				type: 'number',
				required: true,
				default: 240,
			},
			{
				displayName: 'Color',
				name: 'color',

				type: 'number',
				required: true,
				default: 1,
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		return [items];
	}
}
