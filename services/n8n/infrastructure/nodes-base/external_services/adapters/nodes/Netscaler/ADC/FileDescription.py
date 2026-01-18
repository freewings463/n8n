"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Netscaler/ADC/FileDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Netscaler/ADC 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:fileDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Netscaler/ADC/FileDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Netscaler/ADC/FileDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const fileDescription: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a file',
			},
			{
				name: 'Download',
				value: 'download',
				action: 'Download a file',
			},
			{
				name: 'Upload',
				value: 'upload',
				action: 'Upload a file',
			},
		],
		default: 'upload',
		displayOptions: {
			show: {
				resource: ['file'],
			},
		},
	},
	// Upload --------------------------------------------------------------------------
	{
		displayName: 'File Location',
		name: 'fileLocation',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['upload'],
				resource: ['file'],
			},
		},
		default: '/nsconfig/ssl/',
	},
	{
		displayName: 'Input Data Field Name',
		name: 'binaryProperty',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['upload'],
				resource: ['file'],
			},
		},
		default: 'data',
		description: 'The name of the incoming field containing the binary file data to be processed',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		displayOptions: {
			show: {
				operation: ['upload'],
				resource: ['file'],
			},
		},
		options: [
			{
				displayName: 'File Name',
				name: 'fileName',
				type: 'string',
				default: '',
				description: 'Name of the file. It should not include filepath.',
			},
		],
	},
	// Delete, Download ---------------------------------------------------------------
	{
		displayName: 'File Location',
		name: 'fileLocation',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['delete', 'download'],
				resource: ['file'],
			},
		},
		default: '/nsconfig/ssl/',
	},
	{
		displayName: 'File Name',
		name: 'fileName',
		type: 'string',
		default: '',
		required: true,
		description: 'Name of the file. It should not include filepath.',
		displayOptions: {
			show: {
				operation: ['delete', 'download'],
				resource: ['file'],
			},
		},
	},
	{
		displayName: 'Put Output in Field',
		name: 'binaryProperty',
		type: 'string',
		required: true,
		default: 'data',
		description: 'The name of the output field to put the binary file data in',
		displayOptions: {
			show: {
				operation: ['download'],
				resource: ['file'],
			},
		},
	},
];
