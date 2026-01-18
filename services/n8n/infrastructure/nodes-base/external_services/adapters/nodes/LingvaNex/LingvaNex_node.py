"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/LingvaNex/LingvaNex.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/LingvaNex 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:LingvaNex。关键函数/方法:execute、getLanguages。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/LingvaNex/LingvaNex.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/LingvaNex/LingvaNex_node.py

import type {
	IExecuteFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	INodeExecutionData,
	INodePropertyOptions,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { lingvaNexApiRequest } from './GenericFunctions';

export class LingvaNex implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'LingvaNex',
		name: 'lingvaNex',
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:lingvanex.png',
		group: ['output'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Consume LingvaNex API',
		defaults: {
			name: 'LingvaNex',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'lingvaNexApi',
				required: true,
			},
		],
		properties: [
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Translate',
						value: 'translate',
						description: 'Translate data',
						action: 'Translate data',
					},
				],
				default: 'translate',
			},
			// ----------------------------------
			//         All
			// ----------------------------------
			{
				displayName: 'Text',
				name: 'text',
				type: 'string',
				default: '',
				description: 'The input text to translate',
				required: true,
				displayOptions: {
					show: {
						operation: ['translate'],
					},
				},
			},
			{
				// eslint-disable-next-line n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options
				displayName: 'Translate To',
				name: 'translateTo',
				type: 'options',
				typeOptions: {
					loadOptionsMethod: 'getLanguages',
				},
				default: '',
				description:
					'The language to use for translation of the input text, set to one of the language codes listed in <a href="https://cloud.google.com/translate/docs/languages">Language Support</a>. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
				required: true,
				displayOptions: {
					show: {
						operation: ['translate'],
					},
				},
			},
			{
				displayName: 'Additional Options',
				name: 'options',
				type: 'collection',
				placeholder: 'Add option',
				default: {},
				displayOptions: {
					show: {
						operation: ['translate'],
					},
				},
				options: [
					{
						// eslint-disable-next-line n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options
						displayName: 'From',
						name: 'from',
						type: 'options',
						typeOptions: {
							loadOptionsMethod: 'getLanguages',
						},
						default: '',
						description:
							'The language code in the format “language code_code of the country”. If this parameter is not present, the auto-detect language mode is enabled. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
					},
					{
						displayName: 'Platform',
						name: 'platform',
						type: 'string',
						default: 'api',
					},
					{
						displayName: 'Translate Mode',
						name: 'translateMode',
						type: 'string',
						default: '',
						description:
							'Describe the input text format. Possible value is "html" for translating and preserving html structure. If value is not specified or is other than "html" than plain text is translating.',
					},
				],
			},
		],
	};

	methods = {
		loadOptions: {
			async getLanguages(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				const returnData: INodePropertyOptions[] = [];
				const data = await lingvaNexApiRequest.call(
					this,
					'GET',
					'/getLanguages',
					{},
					{ platform: 'api' },
				);
				for (const language of data.result) {
					returnData.push({
						name: language.englishName,
						value: language.full_code,
					});
				}
				return returnData;
			},
		},
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const length = items.length;

		const operation = this.getNodeParameter('operation', 0);
		const responseData = [];
		for (let i = 0; i < length; i++) {
			if (operation === 'translate') {
				const text = this.getNodeParameter('text', i) as string;
				const translateTo = this.getNodeParameter('translateTo', i) as string;
				const options = this.getNodeParameter('options', i);

				const body: IDataObject = {
					data: text,
					to: translateTo,
					platform: 'api',
				};

				Object.assign(body, options);

				const response = await lingvaNexApiRequest.call(this, 'POST', '/translate', body);
				responseData.push(response);
			}
		}
		return [this.helpers.returnJsonArray(responseData)];
	}
}
