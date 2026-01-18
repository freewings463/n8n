"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActionNetwork/descriptions/SignatureDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActionNetwork/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./SharedFields。导出:signatureOperations、signatureFields。关键函数/方法:makeSimpleField。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActionNetwork/descriptions/SignatureDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActionNetwork/descriptions/SignatureDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { makeSimpleField } from './SharedFields';

export const signatureOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['signature'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				action: 'Create a signature',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a signature',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many signatures',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a signature',
			},
		],
		default: 'create',
	},
];

export const signatureFields: INodeProperties[] = [
	// ----------------------------------------
	//            signature: create
	// ----------------------------------------
	{
		displayName: 'Petition ID',
		name: 'petitionId',
		description: 'ID of the petition to sign',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['signature'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Person ID',
		name: 'personId',
		description: 'ID of the person whose signature to create',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['signature'],
				operation: ['create'],
			},
		},
	},
	makeSimpleField('signature', 'create'),
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['signature'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Comments',
				name: 'comments',
				type: 'string',
				default: '',
				description: 'Comments to leave when signing this petition',
			},
		],
	},

	// ----------------------------------------
	//              signature: get
	// ----------------------------------------
	{
		displayName: 'Petition ID',
		name: 'petitionId',
		description: 'ID of the petition whose signature to retrieve',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['signature'],
				operation: ['get'],
			},
		},
	},
	{
		displayName: 'Signature ID',
		name: 'signatureId',
		description: 'ID of the signature to retrieve',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['signature'],
				operation: ['get'],
			},
		},
	},
	makeSimpleField('signature', 'get'),

	// ----------------------------------------
	//            signature: getAll
	// ----------------------------------------
	{
		displayName: 'Petition ID',
		name: 'petitionId',
		description: 'ID of the petition whose signatures to retrieve',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['signature'],
				operation: ['getAll'],
			},
		},
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['signature'],
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
				resource: ['signature'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
	makeSimpleField('signature', 'getAll'),

	// ----------------------------------------
	//            signature: update
	// ----------------------------------------
	{
		displayName: 'Petition ID',
		name: 'petitionId',
		description: 'ID of the petition whose signature to update',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['signature'],
				operation: ['update'],
			},
		},
	},
	{
		displayName: 'Signature ID',
		name: 'signatureId',
		description: 'ID of the signature to update',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['signature'],
				operation: ['update'],
			},
		},
	},
	makeSimpleField('signature', 'update'),
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['signature'],
				operation: ['update'],
			},
		},
		options: [
			{
				displayName: 'Comments',
				name: 'comments',
				type: 'string',
				default: '',
				description: 'Comments to leave when signing this petition',
			},
		],
	},
];
