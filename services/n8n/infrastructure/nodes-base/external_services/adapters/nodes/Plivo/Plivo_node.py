"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Plivo/Plivo.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Plivo 的节点。导入/依赖:外部:无；内部:无；本地:./CallDescription、./GenericFunctions、./MmsDescription、./SmsDescription。导出:Plivo。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Plivo/Plivo.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Plivo/Plivo_node.py

import {
	type IExecuteFunctions,
	type IDataObject,
	type INodeExecutionData,
	type INodeType,
	type INodeTypeDescription,
	NodeConnectionTypes,
} from 'n8n-workflow';

import { callFields, callOperations } from './CallDescription';
import { plivoApiRequest } from './GenericFunctions';
import { mmsFields, mmsOperations } from './MmsDescription';
import { smsFields, smsOperations } from './SmsDescription';

export class Plivo implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Plivo',
		name: 'plivo',
		icon: 'file:plivo.svg',
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Send SMS/MMS messages or make phone calls',
		defaults: {
			name: 'Plivo',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'plivoApi',
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
						name: 'Call',
						value: 'call',
					},
					{
						// eslint-disable-next-line n8n-nodes-base/node-param-resource-with-plural-option
						name: 'MMS',
						value: 'mms',
					},
					{
						name: 'SMS',
						value: 'sms',
					},
				],
				default: 'sms',
				required: true,
			},
			...smsOperations,
			...smsFields,
			...mmsOperations,
			...mmsFields,
			...callOperations,
			...callFields,
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: IDataObject[] = [];

		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);

		for (let i = 0; i < items.length; i++) {
			let responseData;

			if (resource === 'sms') {
				// *********************************************************************
				//                                sms
				// *********************************************************************

				if (operation === 'send') {
					// ----------------------------------
					//          sms: send
					// ----------------------------------

					const body = {
						src: this.getNodeParameter('from', i) as string,
						dst: this.getNodeParameter('to', i) as string,
						text: this.getNodeParameter('message', i) as string,
					} as IDataObject;

					responseData = await plivoApiRequest.call(this, 'POST', '/Message', body);
				}
			} else if (resource === 'call') {
				// *********************************************************************
				//                                call
				// *********************************************************************

				if (operation === 'make') {
					// ----------------------------------
					//            call: make
					// ----------------------------------

					// https://www.plivo.com/docs/voice/api/call#make-a-call

					const body = {
						from: this.getNodeParameter('from', i) as string,
						to: this.getNodeParameter('to', i) as string,
						answer_url: this.getNodeParameter('answer_url', i) as string,
						answer_method: this.getNodeParameter('answer_method', i) as string,
					} as IDataObject;

					responseData = await plivoApiRequest.call(this, 'POST', '/Call', body);
				}
			} else if (resource === 'mms') {
				// *********************************************************************
				//                                mms
				// *********************************************************************

				if (operation === 'send') {
					// ----------------------------------
					//            mss: send
					// ----------------------------------

					// https://www.plivo.com/docs/sms/api/message#send-a-message

					const body = {
						src: this.getNodeParameter('from', i) as string,
						dst: this.getNodeParameter('to', i) as string,
						text: this.getNodeParameter('message', i) as string,
						type: 'mms',
						media_urls: this.getNodeParameter('media_urls', i) as string,
					} as IDataObject;

					responseData = await plivoApiRequest.call(this, 'POST', '/Message', body);
				}
			}

			Array.isArray(responseData)
				? returnData.push(...(responseData as IDataObject[]))
				: returnData.push(responseData as IDataObject);
		}

		return [this.helpers.returnJsonArray(returnData)];
	}
}
