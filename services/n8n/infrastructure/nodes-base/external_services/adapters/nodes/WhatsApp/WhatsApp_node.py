"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/WhatsApp/WhatsApp.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/WhatsApp 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions、./MediaDescription、./MessageFunctions、./MessagesDescription 等2项。导出:WhatsApp。关键函数/方法:createMessage。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/WhatsApp/WhatsApp.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/WhatsApp/WhatsApp_node.py

import type { IExecuteFunctions, INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes, NodeOperationError, SEND_AND_WAIT_OPERATION } from 'n8n-workflow';

import { createMessage, WHATSAPP_BASE_URL } from './GenericFunctions';
import { mediaFields, mediaTypeFields } from './MediaDescription';
import { sanitizePhoneNumber } from './MessageFunctions';
import { messageFields, messageTypeFields } from './MessagesDescription';
import { configureWaitTillDate } from '../../utils/sendAndWait/configureWaitTillDate.util';
import { sendAndWaitWebhooksDescription } from '../../utils/sendAndWait/descriptions';
import {
	getSendAndWaitConfig,
	getSendAndWaitProperties,
	SEND_AND_WAIT_WAITING_TOOLTIP,
	sendAndWaitWebhook,
} from '../../utils/sendAndWait/utils';

const WHATSAPP_CREDENTIALS_TYPE = 'whatsAppApi';

export class WhatsApp implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'WhatsApp Business Cloud',
		name: 'whatsApp',
		icon: 'file:whatsapp.svg',
		group: ['output'],
		version: [1, 1.1],
		defaultVersion: 1.1,
		subtitle: '={{ $parameter["resource"] + ": " + $parameter["operation"] }}',
		description: 'Access WhatsApp API',
		defaults: {
			name: 'WhatsApp Business Cloud',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		waitingNodeTooltip: SEND_AND_WAIT_WAITING_TOOLTIP,
		webhooks: sendAndWaitWebhooksDescription,
		credentials: [
			{
				name: WHATSAPP_CREDENTIALS_TYPE,
				required: true,
			},
		],
		requestDefaults: {
			baseURL: WHATSAPP_BASE_URL,
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Message',
						value: 'message',
					},
					{
						name: 'Media',
						value: 'media',
					},
				],
				default: 'message',
			},
			...messageFields,
			...mediaFields,
			...messageTypeFields,
			...mediaTypeFields,
			...getSendAndWaitProperties([], 'message', undefined, {
				noButtonStyle: true,
				defaultApproveLabel: '✓ Approve',
				defaultDisapproveLabel: '✗ Decline',
			}).filter((p) => p.name !== 'subject'),
		],
	};

	webhook = sendAndWaitWebhook;

	customOperations = {
		message: {
			async [SEND_AND_WAIT_OPERATION](this: IExecuteFunctions) {
				try {
					const phoneNumberId = this.getNodeParameter('phoneNumberId', 0) as string;

					const recipientPhoneNumber = sanitizePhoneNumber(
						this.getNodeParameter('recipientPhoneNumber', 0) as string,
					);

					const config = getSendAndWaitConfig(this);
					const instanceId = this.getInstanceId();

					await this.helpers.httpRequestWithAuthentication.call(
						this,
						WHATSAPP_CREDENTIALS_TYPE,
						createMessage(config, phoneNumberId, recipientPhoneNumber, instanceId),
					);

					const waitTill = configureWaitTillDate(this);

					await this.putExecutionToWait(waitTill);
					return [this.getInputData()];
				} catch (error) {
					throw new NodeOperationError(this.getNode(), error);
				}
			},
		},
	};
}
