"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Misp/descriptions/common.descriptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Misp/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:searchProperties。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Misp/descriptions/common.descriptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Misp/descriptions/common_descriptions.py

import type { INodeProperties } from 'n8n-workflow';

export const searchProperties: INodeProperties[] = [
	{
		displayName: 'Use JSON to Specify Fields',
		name: 'useJson',
		type: 'boolean',
		default: false,
		description: 'Whether to use JSON to specify the fields for the search request',
	},
	{
		displayName: 'JSON',
		name: 'jsonOutput',
		type: 'json',
		description:
			'Get more info at {YOUR_BASE_URL_SPECIFIED_IN_CREDENTIALS}/api/openapi#operation/restSearchAttributes',
		typeOptions: {
			rows: 5,
		},
		default: '{\n  "value": "search value",\n  "type": "text"\n}\n',
		validateType: 'object',
		displayOptions: {
			show: {
				useJson: [true],
			},
		},
	},
	{
		displayName: 'Value',
		name: 'value',
		type: 'string',
		required: true,
		placeholder: 'e.g. 127.0.0.1',
		default: '',
		displayOptions: {
			show: {
				useJson: [false],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				useJson: [false],
			},
		},
		options: [
			{
				displayName: 'Category',
				name: 'category',
				type: 'string',
				placeholder: 'e.g. Internal reference',
				default: '',
			},
			{
				displayName: 'Deleted',
				name: 'deleted',
				type: 'boolean',
				default: false,
			},
			{
				displayName: 'Search All',
				name: 'searchall',
				type: 'string',
				description:
					'Search by matching any tag names, event descriptions, attribute values or attribute comments',
				default: '',
				displayOptions: {
					hide: {
						'/resource': ['attribute'],
					},
				},
			},
			{
				displayName: 'Tags',
				name: 'tags',
				type: 'string',
				placeholder: 'e.g. tag1,tag2',
				hint: 'Comma-separated list of tags',
				default: '',
			},
			{
				displayName: 'Type',
				name: 'type',
				type: 'string',
				placeholder: 'e.g. text',
				default: '',
			},
			{
				displayName: 'Published',
				name: 'published',
				type: 'boolean',
				default: false,
			},
		],
	},
];
