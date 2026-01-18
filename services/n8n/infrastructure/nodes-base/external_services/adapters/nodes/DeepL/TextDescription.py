"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DeepL/TextDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DeepL 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:textOperations。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DeepL/TextDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DeepL/TextDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const textOperations: INodeProperties[] = [
	{
		displayName: 'Text',
		name: 'text',
		type: 'string',
		default: '',
		description: 'Input text to translate',
		required: true,
		displayOptions: {
			show: {
				operation: ['translate'],
			},
		},
	},
	{
		displayName: 'Target Language Name or ID',
		name: 'translateTo',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getLanguages',
		},
		default: '',
		description:
			'Language to translate to. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		required: true,
		displayOptions: {
			show: {
				operation: ['translate'],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		options: [
			{
				displayName: 'Source Language Name or ID',
				name: 'sourceLang',
				type: 'options',
				default: '',
				description:
					'Language to translate from. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
				typeOptions: {
					loadOptionsMethod: 'getLanguages',
				},
			},
			{
				displayName: 'Split Sentences',
				name: 'splitSentences',
				type: 'options',
				default: '1',
				description: 'How the translation engine should split sentences',
				options: [
					{
						name: 'Interpunction Only',
						value: 'nonewlines',
						description: 'Split text on interpunction only, ignoring newlines',
					},
					{
						name: 'No Splitting',
						value: '0',
						description: 'Treat all text as a single sentence',
					},
					{
						name: 'On Punctuation and Newlines',
						value: '1',
						description: 'Split text on interpunction and newlines',
					},
				],
			},
			{
				displayName: 'Preserve Formatting',
				name: 'preserveFormatting',
				type: 'options',
				default: '0',
				description:
					'Whether the translation engine should respect the original formatting, even if it would usually correct some aspects',
				options: [
					{
						name: 'Apply Corrections',
						value: '0',
						description:
							'Fix punctuation at the beginning and end of sentences and fixes lower/upper caseing at the beginning',
					},
					{
						name: 'Do Not Correct',
						value: '1',
						description: 'Keep text as similar as possible to the original',
					},
				],
			},
			{
				displayName: 'Formality',
				name: 'formality',
				type: 'options',
				default: 'default',
				description:
					'How formal or informal the target text should be. May not be supported with all languages.',
				options: [
					{
						name: 'Formal',
						value: 'more',
					},
					{
						name: 'Informal',
						value: 'less',
					},
					{
						name: 'Neutral',
						value: 'default',
					},
				],
			},
		],
	},
];
