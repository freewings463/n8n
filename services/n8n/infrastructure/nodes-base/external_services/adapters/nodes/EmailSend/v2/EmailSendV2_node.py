"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/EmailSend/v2/EmailSendV2.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/EmailSend/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./send.operation、./sendAndWait.operation、./utils、../sendAndWait/descriptions。导出:versionDescription、EmailSendV2。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/EmailSend/v2/EmailSendV2.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/EmailSend/v2/EmailSendV2_node.py

import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeBaseDescription,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes, SEND_AND_WAIT_OPERATION } from 'n8n-workflow';

import * as send from './send.operation';
import * as sendAndWait from './sendAndWait.operation';
import { smtpConnectionTest } from './utils';
import { sendAndWaitWebhooksDescription } from '../../../utils/sendAndWait/descriptions';
import {
	SEND_AND_WAIT_WAITING_TOOLTIP,
	sendAndWaitWebhook,
} from '../../../utils/sendAndWait/utils';

export const versionDescription: INodeTypeDescription = {
	displayName: 'Send Email',
	name: 'emailSend',
	icon: 'fa:envelope',
	group: ['output'],
	version: [2, 2.1],
	description: 'Sends an email using SMTP protocol',
	defaults: {
		name: 'Send Email',
		color: '#00bb88',
	},
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	usableAsTool: true,
	credentials: [
		{
			name: 'smtp',
			required: true,
			testedBy: 'smtpConnectionTest',
		},
	],
	waitingNodeTooltip: SEND_AND_WAIT_WAITING_TOOLTIP,
	webhooks: sendAndWaitWebhooksDescription,
	properties: [
		{
			displayName: 'Resource',
			name: 'resource',
			type: 'hidden',
			noDataExpression: true,
			default: 'email',
			options: [
				{
					name: 'Email',
					value: 'email',
				},
			],
		},
		{
			displayName: 'Operation',
			name: 'operation',
			type: 'options',
			noDataExpression: true,
			default: 'send',
			options: [
				{
					name: 'Send',
					value: 'send',
					action: 'Send an Email',
				},
				{
					name: 'Send and Wait for Response',
					value: SEND_AND_WAIT_OPERATION,
					action: 'Send message and wait for response',
				},
			],
		},
		...send.description,
		...sendAndWait.description,
	],
};

export class EmailSendV2 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			...versionDescription,
		};
	}

	methods = {
		credentialTest: { smtpConnectionTest },
	};

	webhook = sendAndWaitWebhook;

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		let returnData: INodeExecutionData[][] = [];
		const operation = this.getNodeParameter('operation', 0);

		if (operation === SEND_AND_WAIT_OPERATION) {
			returnData = await sendAndWait.execute.call(this);
		}

		if (operation === 'send') {
			returnData = await send.execute.call(this);
		}

		return returnData;
	}
}
