"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Translate/GoogleTranslate.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Translate 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:IGoogleAuthCredentials、GoogleTranslate。关键函数/方法:execute、getLanguages。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Translate/GoogleTranslate.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Translate/GoogleTranslate_node.py

import type {
	IDataObject,
	IExecuteFunctions,
	ILoadOptionsFunctions,
	INodeExecutionData,
	INodePropertyOptions,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { googleApiRequest } from './GenericFunctions';

export interface IGoogleAuthCredentials {
	email: string;
	privateKey: string;
}

export class GoogleTranslate implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Google Translate',
		name: 'googleTranslate',
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:googletranslate.png',
		group: ['input', 'output'],
		version: [1, 2],
		description: 'Translate data using Google Translate',
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		defaults: {
			name: 'Google Translate',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'googleApi',
				required: true,
				displayOptions: {
					show: {
						authentication: ['serviceAccount'],
					},
				},
			},
			{
				name: 'googleTranslateOAuth2Api',
				required: true,
				displayOptions: {
					show: {
						authentication: ['oAuth2'],
					},
				},
			},
		],
		properties: [
			{
				displayName: 'Authentication',
				name: 'authentication',
				type: 'options',
				options: [
					{
						name: 'Service Account',
						value: 'serviceAccount',
					},
					{
						name: 'OAuth2',
						value: 'oAuth2',
					},
				],
				default: 'serviceAccount',
				displayOptions: {
					show: {
						'@version': [1],
					},
				},
			},
			{
				displayName: 'Authentication',
				name: 'authentication',
				type: 'options',
				options: [
					{
						// eslint-disable-next-line n8n-nodes-base/node-param-display-name-miscased
						name: 'OAuth2 (recommended)',
						value: 'oAuth2',
					},
					{
						name: 'Service Account',
						value: 'serviceAccount',
					},
				],
				default: 'oAuth2',
				displayOptions: {
					show: {
						'@version': [2],
					},
				},
			},
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Language',
						value: 'language',
					},
				],
				default: 'language',
			},
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				displayOptions: {
					show: {
						resource: ['language'],
					},
				},
				options: [
					{
						name: 'Translate',
						value: 'translate',
						description: 'Translate data',
						action: 'Translate a language',
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
		],
	};

	methods = {
		loadOptions: {
			async getLanguages(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				const returnData: INodePropertyOptions[] = [];
				const {
					data: { languages },
				} = await googleApiRequest.call(this, 'GET', '/language/translate/v2/languages');
				for (const language of languages) {
					returnData.push({
						name: language.language.toUpperCase(),
						value: language.language,
					});
				}
				return returnData;
			},
		},
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const length = items.length;

		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);
		const responseData: INodeExecutionData[] = [];
		for (let i = 0; i < length; i++) {
			if (resource === 'language') {
				if (operation === 'translate') {
					const text = this.getNodeParameter('text', i) as string;
					const translateTo = this.getNodeParameter('translateTo', i) as string;

					const response = await googleApiRequest.call(this, 'POST', '/language/translate/v2', {
						q: text,
						target: translateTo,
					});

					const [translation] = response.data.translations;

					const executionData = this.helpers.constructExecutionMetaData(
						this.helpers.returnJsonArray(translation as IDataObject),
						{ itemData: { item: i } },
					);

					responseData.push(...executionData);
				}
			}
		}

		return [responseData];
	}
}
