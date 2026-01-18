"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MistralAI/descriptions/document/extractText.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MistralAI/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MistralAI/descriptions/document/extractText.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MistralAI/descriptions/document/extractText_operation.py

import type { INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

const properties: INodeProperties[] = [
	{
		displayName: 'Model',
		name: 'model',
		type: 'options',
		options: [
			{
				name: 'mistral-ocr-latest',
				value: 'mistral-ocr-latest',
			},
		],
		description: 'The OCR model to use',
		required: true,
		default: 'mistral-ocr-latest',
	},
	{
		displayName: 'Document Type',
		name: 'documentType',
		type: 'options',
		options: [
			{
				name: 'Document',
				value: 'document_url',
			},
			{
				name: 'Image',
				value: 'image_url',
			},
		],
		description: 'The type of document to process',
		required: true,
		default: 'document_url',
	},
	{
		displayName: 'Input Type',
		name: 'inputType',
		type: 'options',
		options: [
			{
				name: 'Binary Data',
				value: 'binary',
			},
			{
				name: 'URL',
				value: 'url',
			},
		],
		description: 'How the document will be provided',
		required: true,
		default: 'binary',
		disabledOptions: {
			show: {
				'options.batch': [true],
			},
		},
	},
	{
		displayName: 'Input Binary Field',
		name: 'binaryProperty',
		type: 'string',
		description: 'Name of the input binary field that contains the file to process',
		placeholder: 'e.g. data',
		hint: 'Uploaded document files must not exceed 50 MB in size and should be no longer than 1,000 pages.',
		required: true,
		default: 'data',
		displayOptions: {
			show: {
				inputType: ['binary'],
			},
		},
	},
	{
		displayName: 'URL',
		name: 'url',
		type: 'string',
		description: 'URL of the document or image to process',
		placeholder: 'e.g. https://example.com/document.pdf',
		required: true,
		default: '',
		displayOptions: {
			show: {
				inputType: ['url'],
			},
		},
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		options: [
			{
				displayName: 'Enable Batch Processing',
				name: 'batch',
				type: 'boolean',
				description:
					'Whether to process multiple documents in a single API call (more cost-efficient)',
				default: false,
			},
			{
				displayName: 'Batch Size',
				name: 'batchSize',
				type: 'number',
				description: 'Maximum number of documents to process in a single batch',
				default: 50,
				typeOptions: { maxValue: 2048 },
				required: true,
				displayOptions: {
					show: {
						batch: [true],
					},
				},
			},
			{
				displayName: 'Delete Files After Processing',
				name: 'deleteFiles',
				type: 'boolean',
				default: true,
				description: 'Whether to delete the files on Mistral Cloud after processing',
				displayOptions: {
					show: {
						batch: [true],
					},
				},
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['document'],
		operation: ['extractText'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);
