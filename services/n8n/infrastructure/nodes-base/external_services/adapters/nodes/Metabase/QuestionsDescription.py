"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Metabase/QuestionsDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Metabase 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:questionsOperations、questionsFields。关键函数/方法:function。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Metabase/QuestionsDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Metabase/QuestionsDescription.py

import type { IDataObject, INodeProperties } from 'n8n-workflow';
import { jsonParse } from 'n8n-workflow';

export const questionsOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['questions'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a specific question',
				routing: {
					request: {
						method: 'GET',
						url: '={{"/api/card/" + $parameter.questionId}}',
					},
				},
				action: 'Get a questions',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many questions',
				routing: {
					request: {
						method: 'GET',
						url: '/api/card/',
					},
				},
				action: 'Get many questions',
			},
			{
				name: 'Result Data',
				value: 'resultData',
				description: 'Return the result of the question to a specific file format',
				routing: {
					request: {
						method: 'POST',
						url: '={{"/api/card/" + $parameter.questionId + "/query/" + $parameter.format}}',
						returnFullResponse: true,
						encoding: 'arraybuffer',
					},
					output: {
						postReceive: [
							async function (this, items, responseData) {
								const datatype = this.getNodeParameter('format') as string;

								if (datatype !== 'json') {
									const binaryData = await this.helpers.prepareBinaryData(
										responseData.body as Buffer,
										'data',
										responseData.headers['content-type'] as string,
									);

									// Transform items
									items = items.map((item) => {
										item.json = {};
										item.binary = { ['data']: binaryData };
										return item;
									});
								} else {
									const results = jsonParse<IDataObject[]>(responseData.body as unknown as string);
									items = results.map((result) => {
										return {
											json: {
												...result,
											},
										};
									});
								}
								return items;
							},
						],
					},
				},
				action: 'Get the results from a question',
			},
		],
		default: 'getAll',
	},
];

export const questionsFields: INodeProperties[] = [
	{
		displayName: 'Question ID',
		name: 'questionId',
		type: 'string',
		required: true,
		placeholder: '0',
		displayOptions: {
			show: {
				resource: ['questions'],
				operation: ['get', 'resultData'],
			},
		},
		default: '',
	},
	{
		displayName: 'Format',
		name: 'format',
		type: 'options',
		required: true,
		options: [
			{
				name: 'CSV',
				value: 'csv',
			},
			{
				name: 'JSON',
				value: 'json',
			},
			{
				name: 'XLSX',
				value: 'xlsx',
			},
		],
		default: 'csv',
		displayOptions: {
			show: {
				resource: ['questions'],
				operation: ['resultData'],
			},
		},
	},
];
