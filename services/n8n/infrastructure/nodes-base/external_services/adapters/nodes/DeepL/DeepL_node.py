"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DeepL/DeepL.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DeepL 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions、./TextDescription。导出:DeepL。关键函数/方法:execute、getLanguages。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DeepL/DeepL.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DeepL/DeepL_node.py

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

import { deepLApiRequest } from './GenericFunctions';
import { textOperations } from './TextDescription';

export class DeepL implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'DeepL',
		name: 'deepL',
		icon: { light: 'file:deepl.svg', dark: 'file:deepL.dark.svg' },
		group: ['input', 'output'],
		version: 1,
		description: 'Translate data using DeepL',
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		defaults: {
			name: 'DeepL',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'deepLApi',
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
			...textOperations,
		],
	};

	methods = {
		loadOptions: {
			async getLanguages(this: ILoadOptionsFunctions) {
				const returnData: INodePropertyOptions[] = [];
				const languages = await deepLApiRequest.call(
					this,
					'GET',
					'/languages',
					{},
					{ type: 'target' },
				);
				for (const language of languages) {
					returnData.push({
						name: language.name,
						value: language.language,
					});
				}

				returnData.sort((a, b) => {
					if (a.name < b.name) {
						return -1;
					}
					if (a.name > b.name) {
						return 1;
					}
					return 0;
				});

				return returnData;
			},
		},
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const length = items.length;

		const responseData: INodeExecutionData[] = [];

		for (let i = 0; i < length; i++) {
			try {
				const resource = this.getNodeParameter('resource', i);
				const operation = this.getNodeParameter('operation', i);
				const additionalFields = this.getNodeParameter('additionalFields', i);
				if (resource === 'language') {
					if (operation === 'translate') {
						let body: IDataObject = {};
						const text = this.getNodeParameter('text', i) as string;
						const translateTo = this.getNodeParameter('translateTo', i) as string;
						body = { target_lang: translateTo, text } as IDataObject;

						if (additionalFields.sourceLang !== undefined) {
							body.source_lang = ['EN-GB', 'EN-US'].includes(additionalFields.sourceLang as string)
								? 'EN'
								: additionalFields.sourceLang;
						}

						const { translations } = await deepLApiRequest.call(this, 'GET', '/translate', body);
						const [translation] = translations;
						const translationJsonArray = this.helpers.returnJsonArray(translation as IDataObject[]);
						const executionData = this.helpers.constructExecutionMetaData(translationJsonArray, {
							itemData: { item: i },
						});
						responseData.push(...executionData);
					}
				}
			} catch (error) {
				if (this.continueOnFail()) {
					const executionErrorData = {
						json: {} as IDataObject,
						error: error.message,
						itemIndex: i,
					};
					responseData.push(executionErrorData as INodeExecutionData);
					continue;
				}
				throw error;
			}
		}

		return [responseData];
	}
}
