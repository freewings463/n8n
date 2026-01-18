"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActionNetwork/descriptions/PetitionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActionNetwork/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./SharedFields。导出:petitionOperations、petitionFields。关键函数/方法:makeSimpleField。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActionNetwork/descriptions/PetitionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActionNetwork/descriptions/PetitionDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { makeSimpleField, petitionAdditionalFieldsOptions } from './SharedFields';

export const petitionOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['petition'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a petition',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a petition',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many petitions',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a petition',
			},
		],
		default: 'create',
	},
];

export const petitionFields: INodeProperties[] = [
	// ----------------------------------------
	//             petition: create
	// ----------------------------------------
	{
		displayName: 'Origin System',
		name: 'originSystem',
		description: 'Source where the petition originated',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['petition'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Title',
		name: 'title',
		description: 'Title of the petition to create',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['petition'],
				operation: ['create'],
			},
		},
	},
	makeSimpleField('petition', 'create'),
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['petition'],
				operation: ['create'],
			},
		},
		options: petitionAdditionalFieldsOptions,
	},

	// ----------------------------------------
	//              petition: get
	// ----------------------------------------
	{
		displayName: 'Petition ID',
		name: 'petitionId',
		description: 'ID of the petition to retrieve',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['petition'],
				operation: ['get'],
			},
		},
	},
	makeSimpleField('petition', 'get'),

	// ----------------------------------------
	//             petition: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['petition'],
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
				resource: ['petition'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	makeSimpleField('petition', 'getAll'),

	// ----------------------------------------
	//             petition: update
	// ----------------------------------------
	{
		displayName: 'Petition ID',
		name: 'petitionId',
		description: 'ID of the petition to update',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['petition'],
				operation: ['update'],
			},
		},
	},
	makeSimpleField('petition', 'update'),
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['petition'],
				operation: ['update'],
			},
		},
		options: petitionAdditionalFieldsOptions,
	},
];
