"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Msg91/Msg91.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Msg91 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:Msg91。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Msg91/Msg91.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Msg91/Msg91_node.py

import type {
	IExecuteFunctions,
	IDataObject,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeConnectionTypes, NodeOperationError } from 'n8n-workflow';

import { msg91ApiRequest } from './GenericFunctions';

export class Msg91 implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'MSG91',
		name: 'msg91',

		icon: { light: 'file:msg91.svg', dark: 'file:msg91.dark.svg' },
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Sends transactional SMS via MSG91',
		defaults: {
			name: 'MSG91',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'msg91Api',
				required: true,
			},
		],
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'SMS',
						value: 'sms',
					},
				],
				default: 'sms',
			},
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				displayOptions: {
					show: {
						resource: ['sms'],
					},
				},
				options: [
					{
						name: 'Send',
						value: 'send',
						description: 'Send SMS',
						action: 'Send an SMS',
					},
				],
				default: 'send',
			},
			{
				displayName: 'Sender ID',
				name: 'from',
				type: 'string',
				default: '',
				placeholder: '4155238886',
				required: true,
				displayOptions: {
					show: {
						operation: ['send'],
						resource: ['sms'],
					},
				},
				description: 'The number from which to send the message',
			},
			{
				displayName: 'To',
				name: 'to',
				type: 'string',
				default: '',
				placeholder: '+14155238886',
				required: true,
				displayOptions: {
					show: {
						operation: ['send'],
						resource: ['sms'],
					},
				},
				description: 'The number, with coutry code, to which to send the message',
			},
			{
				displayName: 'Message',
				name: 'message',
				type: 'string',
				default: '',
				required: true,
				displayOptions: {
					show: {
						operation: ['send'],
						resource: ['sms'],
					},
				},
				description: 'The message to send',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: IDataObject[] = [];

		let operation: string;
		let resource: string;

		// For Post
		let body: IDataObject;
		// For Query string
		let qs: IDataObject;

		let requestMethod: IHttpRequestMethods;
		let endpoint: string;

		for (let i = 0; i < items.length; i++) {
			endpoint = '';
			body = {};
			qs = {};

			resource = this.getNodeParameter('resource', i);
			operation = this.getNodeParameter('operation', i);

			if (resource === 'sms') {
				if (operation === 'send') {
					// ----------------------------------
					//         sms:send
					// ----------------------------------

					requestMethod = 'GET';
					endpoint = '/sendhttp.php';

					qs.route = 4;
					qs.country = 0;
					qs.sender = this.getNodeParameter('from', i) as string;
					qs.mobiles = this.getNodeParameter('to', i) as string;
					qs.message = this.getNodeParameter('message', i) as string;
				} else {
					throw new NodeOperationError(
						this.getNode(),
						`The operation "${operation}" is not known!`,
						{ itemIndex: i },
					);
				}
			} else {
				throw new NodeOperationError(this.getNode(), `The resource "${resource}" is not known!`, {
					itemIndex: i,
				});
			}

			const responseData = await msg91ApiRequest.call(this, requestMethod, endpoint, body, qs);

			returnData.push({ requestId: responseData });
		}

		return [this.helpers.returnJsonArray(returnData)];
	}
}
