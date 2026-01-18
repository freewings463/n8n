"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Plivo/CallDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Plivo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:callOperations、callFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Plivo/CallDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Plivo/CallDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const callOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['call'],
			},
		},
		options: [
			{
				name: 'Make',
				value: 'make',
				description: 'Make a voice call',
				action: 'Make a call',
			},
		],
		default: 'make',
	},
];

export const callFields: INodeProperties[] = [
	// ----------------------------------
	//           call: make
	// ----------------------------------
	{
		displayName: 'From',
		name: 'from',
		type: 'string',
		default: '',
		placeholder: '+14156667777',
		description: 'Caller ID for the call to make',
		required: true,
		displayOptions: {
			show: {
				resource: ['call'],
				operation: ['make'],
			},
		},
	},
	{
		displayName: 'To',
		name: 'to',
		type: 'string',
		default: '',
		placeholder: '+14156667778',
		required: true,
		description: 'Phone number to make the call to',
		displayOptions: {
			show: {
				resource: ['call'],
				operation: ['make'],
			},
		},
	},
	{
		displayName: 'Answer Method',
		name: 'answer_method',
		type: 'options',
		required: true,
		description: 'HTTP verb to be used when invoking the Answer URL',
		default: 'POST',
		options: [
			{
				name: 'GET',
				value: 'GET',
			},
			{
				name: 'POST',
				value: 'POST',
			},
		],
		displayOptions: {
			show: {
				resource: ['call'],
				operation: ['make'],
			},
		},
	},
	{
		displayName: 'Answer URL',
		name: 'answer_url',
		type: 'string',
		default: '',
		description:
			'URL to be invoked by Plivo once the call is answered. It should return the XML to handle the call once answered.',
		required: true,
		displayOptions: {
			show: {
				resource: ['call'],
				operation: ['make'],
			},
		},
	},
];
