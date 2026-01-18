"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtable/v2/actions/common.descriptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtable/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:baseRLC、tableRLC、viewRLC、insertUpdateOptions。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtable/v2/actions/common.descriptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtable/v2/actions/common_descriptions.py

import type { INodeProperties } from 'n8n-workflow';

export const baseRLC: INodeProperties = {
	displayName: 'Base',
	name: 'base',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	// description: 'The Airtable Base in which to operate on',
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'baseSearch',
				searchable: true,
			},
		},
		{
			displayName: 'By URL',
			name: 'url',
			type: 'string',
			placeholder: 'e.g. https://airtable.com/app12DiScdfes/tbl9WvGeEPa6lZyVq/viwHdfasdfeieg5p',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: 'https://airtable.com/([a-zA-Z0-9]{2,})/.*',
						errorMessage: 'Not a valid Airtable Base URL',
					},
				},
			],
			extractValue: {
				type: 'regex',
				regex: 'https://airtable.com/([a-zA-Z0-9]{2,})',
			},
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: '[a-zA-Z0-9]{2,}',
						errorMessage: 'Not a valid Airtable Base ID',
					},
				},
			],
			placeholder: 'e.g. appD3dfaeidke',
			url: '=https://airtable.com/{{$value}}',
		},
	],
};

export const tableRLC: INodeProperties = {
	displayName: 'Table',
	name: 'table',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	typeOptions: {
		loadOptionsDependsOn: ['base.value'],
	},
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'tableSearch',
				searchable: true,
			},
		},
		{
			displayName: 'By URL',
			name: 'url',
			type: 'string',
			placeholder: 'https://airtable.com/app12DiScdfes/tblAAAAAAAAAAAAA/viwHdfasdfeieg5p',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: 'https://airtable.com/[a-zA-Z0-9]{2,}/([a-zA-Z0-9]{2,})/.*',
						errorMessage: 'Not a valid Airtable Table URL',
					},
				},
			],
			extractValue: {
				type: 'regex',
				regex: 'https://airtable.com/[a-zA-Z0-9]{2,}/([a-zA-Z0-9]{2,})',
			},
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: '[a-zA-Z0-9]{2,}',
						errorMessage: 'Not a valid Airtable Table ID',
					},
				},
			],
			placeholder: 'tbl3dirwqeidke',
		},
	],
};

export const viewRLC: INodeProperties = {
	displayName: 'View',
	name: 'view',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'viewSearch',
				searchable: true,
			},
		},
		{
			displayName: 'By URL',
			name: 'url',
			type: 'string',
			placeholder: 'https://airtable.com/app12DiScdfes/tblAAAAAAAAAAAAA/viwHdfasdfeieg5p',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: 'https://airtable.com/[a-zA-Z0-9]{2,}/[a-zA-Z0-9]{2,}/([a-zA-Z0-9]{2,})/.*',
						errorMessage: 'Not a valid Airtable View URL',
					},
				},
			],
			extractValue: {
				type: 'regex',
				regex: 'https://airtable.com/[a-zA-Z0-9]{2,}/[a-zA-Z0-9]{2,}/([a-zA-Z0-9]{2,})',
			},
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: '[a-zA-Z0-9]{2,}',
						errorMessage: 'Not a valid Airtable View ID',
					},
				},
			],
			placeholder: 'viw3dirwqeidke',
		},
	],
};

export const insertUpdateOptions: INodeProperties[] = [
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Typecast',
				name: 'typecast',
				type: 'boolean',
				default: false,
				description:
					'Whether the Airtable API should attempt mapping of string values for linked records & select options',
			},
			{
				displayName: 'Ignore Fields From Input',
				name: 'ignoreFields',
				type: 'string',
				requiresDataPath: 'multiple',
				displayOptions: {
					show: {
						'/columns.mappingMode': ['autoMapInputData'],
					},
				},
				default: '',
				description: 'Comma-separated list of fields in input to ignore when updating',
			},
			{
				displayName: 'Update All Matches',
				name: 'updateAllMatches',
				type: 'boolean',
				default: false,
				description:
					'Whether to update all records matching the value in the "Column to Match On". If not set, only the first matching record will be updated.',
				displayOptions: {
					show: {
						'/operation': ['update', 'upsert'],
					},
				},
			},
		],
	},
];
