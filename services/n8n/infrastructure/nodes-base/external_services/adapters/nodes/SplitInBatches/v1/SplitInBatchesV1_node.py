"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SplitInBatches/v1/SplitInBatchesV1.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SplitInBatches/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:SplitInBatchesV1。关键函数/方法:execute、addSourceOverwrite、getPairedItemInformation。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SplitInBatches/v1/SplitInBatchesV1.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SplitInBatches/v1/SplitInBatchesV1_node.py

import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	IPairedItemData,
} from 'n8n-workflow';
import { NodeConnectionTypes, deepCopy } from 'n8n-workflow';

export class SplitInBatchesV1 implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Split In Batches',
		name: 'splitInBatches',
		icon: 'fa:th-large',
		group: ['organization'],
		version: 1,
		description: 'Split data into batches and iterate over each batch',
		defaults: {
			name: 'Split In Batches',
			color: '#007755',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName:
					'You may not need this node — n8n nodes automatically run once for each input item. <a href="https://docs.n8n.io/getting-started/key-concepts/looping.html#using-loops-in-n8n" target="_blank">More info</a>',
				name: 'splitInBatchesNotice',
				type: 'notice',
				default: '',
			},
			{
				displayName: 'Batch Size',
				name: 'batchSize',
				type: 'number',
				typeOptions: {
					minValue: 1,
				},
				default: 10,
				description: 'The number of items to return with each call',
			},
			{
				displayName: 'Options',
				name: 'options',
				type: 'collection',
				placeholder: 'Add option',
				default: {},
				options: [
					{
						displayName: 'Reset',
						name: 'reset',
						type: 'boolean',
						default: false,
						description:
							'Whether the node will be reset and so with the current input-data newly initialized',
					},
				],
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][] | null> {
		// Get the input data and create a new array so that we can remove
		// items without a problem
		const items = this.getInputData().slice();

		const nodeContext = this.getContext('node');

		const batchSize = this.getNodeParameter('batchSize', 0) as number;

		const returnItems: INodeExecutionData[] = [];

		const options = this.getNodeParameter('options', 0, {});

		if (nodeContext.items === undefined || options.reset === true) {
			// Is the first time the node runs

			const sourceData = this.getInputSourceData();

			nodeContext.currentRunIndex = 0;
			nodeContext.maxRunIndex = Math.ceil(items.length / batchSize);
			nodeContext.sourceData = deepCopy(sourceData);

			// Get the items which should be returned
			returnItems.push.apply(returnItems, items.splice(0, batchSize));

			// Set the other items to be saved in the context to return at later runs
			nodeContext.items = [...items];
		} else {
			// The node has been called before. So return the next batch of items.
			nodeContext.currentRunIndex += 1;
			returnItems.push.apply(
				returnItems,
				(nodeContext.items as INodeExecutionData[]).splice(0, batchSize),
			);

			const addSourceOverwrite = (pairedItem: IPairedItemData | number): IPairedItemData => {
				if (typeof pairedItem === 'number') {
					return {
						item: pairedItem,
						sourceOverwrite: nodeContext.sourceData,
					};
				}

				return {
					...pairedItem,
					sourceOverwrite: nodeContext.sourceData,
				};
			};

			function getPairedItemInformation(
				item: INodeExecutionData,
			): IPairedItemData | IPairedItemData[] {
				if (item.pairedItem === undefined) {
					return {
						item: 0,
						sourceOverwrite: nodeContext.sourceData,
					};
				}

				if (Array.isArray(item.pairedItem)) {
					return item.pairedItem.map(addSourceOverwrite);
				}

				return addSourceOverwrite(item.pairedItem);
			}

			returnItems.map((item) => {
				item.pairedItem = getPairedItemInformation(item);
			});
		}

		nodeContext.noItemsLeft = nodeContext.items.length === 0;

		if (returnItems.length === 0) {
			// No data left to return so stop execution of the branch
			return null;
		}

		return [returnItems];
	}
}
