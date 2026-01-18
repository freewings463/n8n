"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/MicrosoftOutlookTrigger.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:luxon；内部:无；本地:./trigger/GenericFunctions、./trigger/MessageDescription、./v2/methods。导出:MicrosoftOutlookTrigger。关键函数/方法:poll、startDate。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/MicrosoftOutlookTrigger.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/MicrosoftOutlookTrigger_node.py

import { DateTime } from 'luxon';
import {
	type IPollFunctions,
	type INodeExecutionData,
	type INodeType,
	type INodeTypeDescription,
	NodeConnectionTypes,
} from 'n8n-workflow';

import { getPollResponse } from './trigger/GenericFunctions';
import { properties as messageProperties } from './trigger/MessageDescription';
import { loadOptions } from './v2/methods';

export class MicrosoftOutlookTrigger implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Microsoft Outlook Trigger',
		name: 'microsoftOutlookTrigger',
		icon: 'file:outlook.svg',
		group: ['trigger'],
		version: 1,
		description:
			'Fetches emails from Microsoft Outlook and starts the workflow on specified polling intervals.',
		subtitle: '={{"Microsoft Outlook Trigger"}}',
		defaults: {
			name: 'Microsoft Outlook Trigger',
		},
		credentials: [
			{
				name: 'microsoftOutlookOAuth2Api',
				required: true,
			},
		],
		polling: true,
		inputs: [],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName: 'Trigger On',
				name: 'event',
				type: 'options',
				default: 'messageReceived',
				options: [
					{
						name: 'Message Received',
						value: 'messageReceived',
					},
				],
			},
			...messageProperties,
		],
	};

	methods = { loadOptions };

	async poll(this: IPollFunctions): Promise<INodeExecutionData[][] | null> {
		const webhookData = this.getWorkflowStaticData('node');
		let responseData;

		const now = DateTime.now().toISO();
		const startDate = (webhookData.lastTimeChecked as string) || now;
		const endDate = now;
		try {
			const pollStartDate = startDate;
			const pollEndDate = endDate;

			responseData = await getPollResponse.call(this, pollStartDate, pollEndDate);

			if (!responseData?.length) {
				webhookData.lastTimeChecked = endDate;
				return null;
			}
		} catch (error) {
			if (this.getMode() === 'manual' || !webhookData.lastTimeChecked) {
				throw error;
			}
			const workflow = this.getWorkflow();
			const node = this.getNode();
			this.logger.error(
				`There was a problem in '${node.name}' node in workflow '${workflow.id}': '${error.description}'`,
				{
					node: node.name,
					workflowId: workflow.id,
					error,
				},
			);
		}

		webhookData.lastTimeChecked = endDate;

		if (Array.isArray(responseData) && responseData.length) {
			return [responseData];
		}

		return null;
	}
}
