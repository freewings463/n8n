"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Yourls/Yourls.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Yourls 的节点。导入/依赖:外部:无；内部:无；本地:./GenericFunctions、./UrlDescription。导出:Yourls。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Yourls/Yourls.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Yourls/Yourls_node.py

import {
	type IExecuteFunctions,
	type IDataObject,
	type INodeExecutionData,
	type INodeType,
	type INodeTypeDescription,
	NodeConnectionTypes,
} from 'n8n-workflow';

import { yourlsApiRequest } from './GenericFunctions';
import { urlFields, urlOperations } from './UrlDescription';

export class Yourls implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Yourls',
		name: 'yourls',
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:yourls.png',
		group: ['input'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Consume Yourls API',
		defaults: {
			name: 'Yourls',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'yourlsApi',
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
						name: 'URL',
						value: 'url',
					},
				],
				default: 'url',
			},
			...urlOperations,
			...urlFields,
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: IDataObject[] = [];
		const length = items.length;
		const qs: IDataObject = {};
		let responseData;
		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);
		for (let i = 0; i < length; i++) {
			try {
				if (resource === 'url') {
					if (operation === 'shorten') {
						const url = this.getNodeParameter('url', i) as string;
						const additionalFields = this.getNodeParameter('additionalFields', i);
						qs.url = url;
						qs.action = 'shorturl';
						Object.assign(qs, additionalFields);
						responseData = await yourlsApiRequest.call(this, 'GET', {}, qs);
					}

					if (operation === 'expand') {
						const shortUrl = this.getNodeParameter('shortUrl', i) as string;
						qs.shorturl = shortUrl;
						qs.action = 'expand';
						responseData = await yourlsApiRequest.call(this, 'GET', {}, qs);
					}

					if (operation === 'stats') {
						const shortUrl = this.getNodeParameter('shortUrl', i) as string;
						qs.shorturl = shortUrl;
						qs.action = 'url-stats';
						responseData = await yourlsApiRequest.call(this, 'GET', {}, qs);
						responseData = responseData.link;
					}
				}
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
