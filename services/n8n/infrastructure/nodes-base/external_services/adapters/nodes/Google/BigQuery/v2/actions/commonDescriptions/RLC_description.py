"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/BigQuery/v2/actions/commonDescriptions/RLC.description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/BigQuery 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:projectRLC、datasetRLC、tableRLC。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/BigQuery/v2/actions/commonDescriptions/RLC.description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/BigQuery/v2/actions/commonDescriptions/RLC_description.py

import type { INodeProperties } from 'n8n-workflow';

export const projectRLC: INodeProperties = {
	displayName: 'Project',
	name: 'projectId',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'searchProjects',
				searchable: true,
			},
		},
		{
			displayName: 'By URL',
			name: 'url',
			type: 'string',
			extractValue: {
				type: 'regex',
				regex: 'https:\\/\\/console.cloud.google.com\\/bigquery\\?project=([0-9a-zA-Z\\-_]+).{0,}',
			},
			validation: [
				{
					type: 'regex',
					properties: {
						regex:
							'https:\\/\\/console.cloud.google.com\\/bigquery\\?project=([0-9a-zA-Z\\-_]+).{0,}',
						errorMessage: 'Not a valid BigQuery Project URL',
					},
				},
			],
		},
		{
			displayName: 'By ID',
			name: 'id',
			type: 'string',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: '[a-zA-Z0-9\\-_]{2,}',
						errorMessage: 'Not a valid BigQuery Project ID',
					},
				},
			],
			url: '=https://console.cloud.google.com/bigquery?project={{$value}}',
		},
	],
	description: 'Projects to which you have been granted any project role',
};

export const datasetRLC: INodeProperties = {
	displayName: 'Dataset',
	name: 'datasetId',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'searchDatasets',
				searchable: true,
			},
		},
		{
			displayName: 'By ID',
			name: 'id',
			type: 'string',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: '[a-zA-Z0-9\\-_]{2,}',
						errorMessage: 'Not a valid Dataset ID',
					},
				},
			],
		},
	],
};

export const tableRLC: INodeProperties = {
	displayName: 'Table',
	name: 'tableId',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'searchTables',
				searchable: true,
			},
		},
		{
			displayName: 'By ID',
			name: 'id',
			type: 'string',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: '[a-zA-Z0-9\\-_]{2,}',
						errorMessage: 'Not a valid Table ID',
					},
				},
			],
		},
	],
};
