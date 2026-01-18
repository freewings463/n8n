"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/companyReport/get/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:companyReportGetDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/companyReport/get/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/companyReport/get/description.py

import type { INodeProperties } from 'n8n-workflow';

export const companyReportGetDescription: INodeProperties[] = [
	{
		displayName: 'Report ID',
		name: 'reportId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['companyReport'],
			},
		},
		default: '',
		description:
			'ID of the report. You can get the report number by hovering over the report name on the reports page and grabbing the ID.',
	},
	{
		displayName: 'Format',
		name: 'format',
		type: 'options',
		options: [
			{
				name: 'CSV',
				value: 'CSV',
			},
			{
				name: 'JSON',
				value: 'JSON',
			},
			{
				name: 'PDF',
				value: 'PDF',
			},
			{
				name: 'XLS',
				value: 'XLS',
			},
			{
				name: 'XML',
				value: 'XML',
			},
		],
		required: true,
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['companyReport'],
			},
		},
		default: 'JSON',
		description: 'The output format for the report',
	},
	{
		displayName: 'Put Output In Field',
		name: 'output',
		type: 'string',
		default: 'data',
		required: true,
		description: 'The name of the output field to put the binary file data in',
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['companyReport'],
			},
			hide: {
				format: ['JSON'],
			},
		},
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['companyReport'],
			},
		},
		options: [
			{
				displayName: 'Duplicate Field Filtering',
				name: 'fd',
				type: 'boolean',
				default: true,
				description: 'Whether to apply the standard duplicate field filtering or not',
			},
			{
				displayName: 'Only Current',
				name: 'onlyCurrent',
				type: 'boolean',
				default: true,
				description: 'Whether to hide future dated values from the history table fields or not',
			},
		],
	},
];
