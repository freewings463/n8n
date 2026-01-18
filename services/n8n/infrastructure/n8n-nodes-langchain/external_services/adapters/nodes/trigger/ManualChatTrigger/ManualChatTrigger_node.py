"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/trigger/ManualChatTrigger/ManualChatTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/trigger/ManualChatTrigger 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:ManualChatTrigger。关键函数/方法:trigger、manualTriggerFunction。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/trigger/ManualChatTrigger/ManualChatTrigger.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/trigger/ManualChatTrigger/ManualChatTrigger_node.py

import {
	type ITriggerFunctions,
	type INodeType,
	type INodeTypeDescription,
	type ITriggerResponse,
	NodeConnectionTypes,
} from 'n8n-workflow';

export class ManualChatTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Manual Chat Trigger',
		name: 'manualChatTrigger',
		icon: 'fa:comments',
		group: ['trigger'],
		version: [1, 1.1],
		description: 'Runs the flow on new manual chat message',
		eventTriggerDescription: '',
		maxNodes: 1,
		hidden: true,
		defaults: {
			name: 'When chat message received',
			color: '#909298',
		},
		codex: {
			categories: ['Core Nodes'],
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-langchain.chattrigger/',
					},
				],
			},
			subcategories: {
				'Core Nodes': ['Other Trigger Nodes'],
			},
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName:
					'This node is where a manual chat workflow execution starts. To make one, go back to the canvas and click ‘Chat’',
				name: 'notice',
				type: 'notice',
				default: '',
			},
			{
				// eslint-disable-next-line n8n-nodes-base/node-param-display-name-miscased
				displayName: 'Chat and execute workflow',
				name: 'openChat',
				type: 'button',
				typeOptions: {
					buttonConfig: {
						action: 'openChat',
					},
				},
				default: '',
			},
		],
	};

	async trigger(this: ITriggerFunctions): Promise<ITriggerResponse> {
		const manualTriggerFunction = async () => {
			this.emit([this.helpers.returnJsonArray([{}])]);
		};

		return {
			manualTriggerFunction,
		};
	}
}
