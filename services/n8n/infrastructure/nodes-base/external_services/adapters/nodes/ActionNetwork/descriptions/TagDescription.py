"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActionNetwork/descriptions/TagDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActionNetwork/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./SharedFields。导出:tagOperations、tagFields。关键函数/方法:makeSimpleField。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActionNetwork/descriptions/TagDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActionNetwork/descriptions/TagDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { makeSimpleField } from './SharedFields';

export const tagOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['tag'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a tag',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a tag',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many tags',
			},
		],
		default: 'create',
	},
];

export const tagFields: INodeProperties[] = [
	// ----------------------------------------
	//               tag: create
	// ----------------------------------------
	{
		displayName: 'Name',
		name: 'name',
		description: 'Name of the tag to create',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['tag'],
				operation: ['create'],
			},
		},
	},
	makeSimpleField('tag', 'create'),

	// ----------------------------------------
	//                 tag: get
	// ----------------------------------------
	{
		displayName: 'Tag ID',
		name: 'tagId',
		description: 'ID of the tag to retrieve',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['tag'],
				operation: ['get'],
			},
		},
	},
	makeSimpleField('tag', 'get'),

	// ----------------------------------------
	//               tag: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['tag'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: 50,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
		},
		displayOptions: {
			show: {
				resource: ['tag'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	makeSimpleField('tag', 'getAll'),
];
