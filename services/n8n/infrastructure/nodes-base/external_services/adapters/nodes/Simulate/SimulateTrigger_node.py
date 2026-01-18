"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Simulate/SimulateTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Simulate 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./methods。导出:SimulateTrigger。关键函数/方法:trigger、manualTriggerFunction。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Simulate/SimulateTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Simulate/SimulateTrigger_node.py

import { sleep, NodeOperationError, jsonParse, NodeConnectionTypes } from 'n8n-workflow';
import type {
	IDataObject,
	ITriggerFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	ITriggerResponse,
} from 'n8n-workflow';

import {
	executionDurationProperty,
	iconSelector,
	jsonOutputProperty,
	subtitleProperty,
} from './descriptions';
import { loadOptions } from './methods';

export class SimulateTrigger implements INodeType {
	description: INodeTypeDescription = {
		hidden: true,
		displayName: 'Simulate Trigger',
		name: 'simulateTrigger',
		subtitle: '={{$parameter.subtitle || undefined}}',
		icon: 'fa:arrow-right',
		group: ['trigger'],
		version: 1,
		description: 'Simulate a trigger node',
		defaults: {
			name: 'Simulate Trigger',
			color: '#b0b0b0',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{ ...iconSelector, default: 'n8n-nodes-base.manualTrigger' },
			subtitleProperty,
			{ ...jsonOutputProperty, displayName: 'Output (JSON)' },
			executionDurationProperty,
		],
	};

	methods = { loadOptions };

	async trigger(this: ITriggerFunctions): Promise<ITriggerResponse> {
		const returnItems: INodeExecutionData[] = [];

		let jsonOutput = this.getNodeParameter('jsonOutput', 0);

		if (typeof jsonOutput === 'string') {
			try {
				jsonOutput = jsonParse<IDataObject>(jsonOutput);
			} catch (error) {
				throw new NodeOperationError(this.getNode(), 'Invalid JSON');
			}
		}

		if (!Array.isArray(jsonOutput)) {
			jsonOutput = [jsonOutput];
		}

		for (const item of jsonOutput as IDataObject[]) {
			returnItems.push({ json: item });
		}

		const executionDuration = this.getNodeParameter('executionDuration', 0) as number;

		if (executionDuration > 0) {
			await sleep(executionDuration);
		}

		const manualTriggerFunction = async () => {
			this.emit([returnItems]);
		};

		return {
			manualTriggerFunction,
		};
	}
}
