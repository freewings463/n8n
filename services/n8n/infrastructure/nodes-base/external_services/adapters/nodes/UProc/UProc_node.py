"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/UProc/UProc.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/UProc 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions、./GroupDescription、./ToolDescription。导出:UProc。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/UProc/UProc.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/UProc/UProc_node.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import type {
	IExecuteFunctions,
	IDataObject,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { uprocApiRequest } from './GenericFunctions';
import { groupOptions } from './GroupDescription';
import { toolOperations, toolParameters } from './ToolDescription';

export class UProc implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'uProc',
		name: 'uproc',
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:uproc.png',
		group: ['output'],
		version: 1,
		subtitle: '={{$parameter["tool"]}}',
		description: 'Consume uProc API',
		defaults: {
			name: 'uProc',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'uprocApi',
				required: true,
			},
		],
		properties: [
			...groupOptions,
			...toolOperations,
			...toolParameters,
			{
				displayName: 'Additional Options',
				name: 'additionalOptions',
				type: 'collection',
				placeholder: 'Add option',
				default: {},
				displayOptions: {
					show: {
						group: [
							'audio',
							'communication',
							'company',
							'finance',
							'geographic',
							'image',
							'internet',
							'personal',
							'product',
							'security',
							'text',
						],
					},
				},
				options: [
					{
						displayName: 'Data Webhook',
						name: 'dataWebhook',
						type: 'string',
						description: 'URL to send tool response when tool has resolved your request',
						default: '',
					},
				],
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: IDataObject[] = [];
		const length = items.length;
		let responseData;
		const group = this.getNodeParameter('group', 0) as string;
		const tool = this.getNodeParameter('tool', 0) as string;
		const additionalOptions = this.getNodeParameter('additionalOptions', 0) as IDataObject;

		const dataWebhook = additionalOptions.dataWebhook as string;

		interface LooseObject {
			[key: string]: any;
		}

		const fields = toolParameters
			.filter((field) => {
				return (
					field?.displayOptions?.show?.group &&
					field.displayOptions.show.tool &&
					field.displayOptions.show.group.indexOf(group) !== -1 &&
					field.displayOptions.show.tool.indexOf(tool) !== -1
				);
			})
			.map((field) => {
				return field.name;
			});

		for (let i = 0; i < length; i++) {
			try {
				const toolKey = tool.replace(/([A-Z]+)/g, '-$1').toLowerCase();
				const body: LooseObject = {
					processor: toolKey,
					params: {},
				};

				fields.forEach((field) => {
					if (field?.length) {
						const data = this.getNodeParameter(field, i) as string;
						body.params[field] = data + '';
					}
				});

				if (dataWebhook?.length) {
					body.callback = {};
				}

				if (dataWebhook?.length) {
					body.callback.data = dataWebhook;
				}

				//Change to multiple requests
				responseData = await uprocApiRequest.call(this, 'POST', body);

				if (Array.isArray(responseData)) {
					returnData.push.apply(returnData, responseData as IDataObject[]);
				} else {
					returnData.push(responseData as IDataObject);
				}
			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({ error: error.message });
					continue;
				}
				throw error;
			}
		}
		return [this.helpers.returnJsonArray(returnData)];
	}
}
