"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Transform/RemoveDuplicates/v1/RemoveDuplicatesV1.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Transform/RemoveDuplicates 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../utils。导出:RemoveDuplicatesV1。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Transform/RemoveDuplicates/v1/RemoveDuplicatesV1.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Transform/RemoveDuplicates/v1/RemoveDuplicatesV1_node.py

import { NodeConnectionTypes } from 'n8n-workflow';
import type {
	INodeTypeBaseDescription,
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';

import { removeDuplicateInputItems } from '../utils';

const versionDescription: INodeTypeDescription = {
	displayName: 'Remove Duplicates',
	name: 'removeDuplicates',
	icon: 'file:removeDuplicates.svg',
	group: ['transform'],
	subtitle: '',
	version: [1, 1.1],
	description: 'Delete items with matching field values',
	defaults: {
		name: 'Remove Duplicates',
	},
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	properties: [
		{
			displayName: 'Compare',
			name: 'compare',
			type: 'options',
			options: [
				{
					name: 'All Fields',
					value: 'allFields',
				},
				{
					name: 'All Fields Except',
					value: 'allFieldsExcept',
				},
				{
					name: 'Selected Fields',
					value: 'selectedFields',
				},
			],
			default: 'allFields',
			description: 'The fields of the input items to compare to see if they are the same',
		},
		{
			displayName: 'Fields To Exclude',
			name: 'fieldsToExclude',
			type: 'string',
			placeholder: 'e.g. email, name',
			requiresDataPath: 'multiple',
			description: 'Fields in the input to exclude from the comparison',
			default: '',
			displayOptions: {
				show: {
					compare: ['allFieldsExcept'],
				},
			},
		},
		{
			displayName: 'Fields To Compare',
			name: 'fieldsToCompare',
			type: 'string',
			placeholder: 'e.g. email, name',
			requiresDataPath: 'multiple',
			description: 'Fields in the input to add to the comparison',
			default: '',
			displayOptions: {
				show: {
					compare: ['selectedFields'],
				},
			},
		},
		{
			displayName: 'Options',
			name: 'options',
			type: 'collection',
			placeholder: 'Add Field',
			default: {},
			displayOptions: {
				show: {
					compare: ['allFieldsExcept', 'selectedFields'],
				},
			},
			options: [
				{
					displayName: 'Disable Dot Notation',
					name: 'disableDotNotation',
					type: 'boolean',
					default: false,
					description:
						'Whether to disallow referencing child fields using `parent.child` in the field name',
				},
				{
					displayName: 'Remove Other Fields',
					name: 'removeOtherFields',
					type: 'boolean',
					default: false,
					description:
						'Whether to remove any fields that are not being compared. If disabled, will keep the values from the first of the duplicates.',
				},
			],
		},
	],
};
export class RemoveDuplicatesV1 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			...versionDescription,
		};
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		return removeDuplicateInputItems(this, items);
	}
}
