"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SseTrigger/SseTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SseTrigger 的节点。导入/依赖:外部:eventsource；内部:n8n-workflow；本地:无。导出:SseTrigger。关键函数/方法:trigger、closeFunction。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SseTrigger/SseTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SseTrigger/SseTrigger_node.py

import EventSource from 'eventsource';
import type {
	IDataObject,
	ITriggerFunctions,
	INodeType,
	INodeTypeDescription,
	ITriggerResponse,
} from 'n8n-workflow';
import { NodeConnectionTypes, jsonParse } from 'n8n-workflow';

export class SseTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'SSE Trigger',
		name: 'sseTrigger',
		icon: 'fa:cloud-download-alt',
		iconColor: 'dark-blue',
		group: ['trigger'],
		version: 1,
		description: 'Triggers the workflow when Server-Sent Events occur',
		eventTriggerDescription: '',
		activationMessage: 'You can now make calls to your SSE URL to trigger executions.',
		defaults: {
			name: 'SSE Trigger',
			color: '#225577',
		},
		triggerPanel: {
			header: '',
			executionsHelp: {
				inactive:
					"<b>While building your workflow</b>, click the 'execute step' button, then trigger an SSE event. This will trigger an execution, which will show up in this editor.<br /> <br /><b>Once you're happy with your workflow</b>, publish it. Then every time a change is detected, the workflow will execute. These executions will show up in the <a data-key='executions'>executions list</a>, but not in the editor.",
				active:
					"<b>While building your workflow</b>, click the 'execute step' button, then trigger an SSE event. This will trigger an execution, which will show up in this editor.<br /> <br /><b>Your workflow will also execute automatically</b>, since it's activated. Every time a change is detected, this node will trigger an execution. These executions will show up in the <a data-key='executions'>executions list</a>, but not in the editor.",
			},
			activationHint:
				'Once you’ve finished building your workflow, publish it to have it also listen continuously (you just won’t see those executions here).',
		},
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName: 'URL',
				name: 'url',
				type: 'string',
				default: '',
				placeholder: 'http://example.com',
				description: 'The URL to receive the SSE from',
				required: true,
			},
		],
	};

	async trigger(this: ITriggerFunctions): Promise<ITriggerResponse> {
		const url = this.getNodeParameter('url') as string;

		const eventSource = new EventSource(url);

		eventSource.onmessage = (event) => {
			const eventData = jsonParse<IDataObject>(event.data as string, {
				errorMessage: 'Invalid JSON for event data',
			});
			this.emit([this.helpers.returnJsonArray([eventData])]);
		};

		async function closeFunction() {
			eventSource.close();
		}

		return {
			closeFunction,
		};
	}
}
