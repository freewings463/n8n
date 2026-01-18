"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Tapfiliate/AffiliateMetadataDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Tapfiliate 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:affiliateMetadataOperations、affiliateMetadataFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Tapfiliate/AffiliateMetadataDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Tapfiliate/AffiliateMetadataDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const affiliateMetadataOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['affiliateMetadata'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add metadata to affiliate',
				action: 'Add metadata to an affiliate',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove metadata from affiliate',
				action: 'Remove metadata from an affiliate',
			},
			{
				name: 'Update',
				value: 'update',
				description: "Update affiliate's metadata",
				action: 'Update metadata for an affiliate',
			},
		],
		default: 'add',
	},
];

export const affiliateMetadataFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                         affiliateMetadata:add                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Affiliate ID',
		name: 'affiliateId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['affiliateMetadata'],
				operation: ['add'],
			},
		},
		description: 'The ID of the affiliate',
	},
	{
		displayName: 'Metadata',
		name: 'metadataUi',
		placeholder: 'Add Metadata',
		type: 'fixedCollection',
		displayOptions: {
			show: {
				resource: ['affiliateMetadata'],
				operation: ['add'],
			},
		},
		default: {},
		typeOptions: {
			multipleValues: true,
		},
		description: 'Meta data',
		options: [
			{
				name: 'metadataValues',
				displayName: 'Metadata',
				values: [
					{
						displayName: 'Key',
						name: 'key',
						type: 'string',
						default: '',
						description: 'Name of the metadata key to add',
					},
					{
						displayName: 'Value',
						name: 'value',
						type: 'string',
						default: '',
						description: 'Value to set for the metadata key',
					},
				],
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                          ffiliateMetadata:remove                           */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Affiliate ID',
		name: 'affiliateId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['affiliateMetadata'],
				operation: ['remove'],
			},
		},
		description: 'The ID of the affiliate',
	},
	{
		displayName: 'Key',
		name: 'key',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['affiliateMetadata'],
				operation: ['remove'],
			},
		},
		default: '',
		description: 'Name of the metadata key to remove',
	},

	/* -------------------------------------------------------------------------- */
	/*                         affiliateMetadata:update                           */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Affiliate ID',
		name: 'affiliateId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['affiliateMetadata'],
				operation: ['update'],
			},
		},
		description: 'The ID of the affiliate',
	},
	{
		displayName: 'Key',
		name: 'key',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['affiliateMetadata'],
				operation: ['update'],
			},
		},
		default: '',
		description: 'Name of the metadata key to update',
	},
	{
		displayName: 'Value',
		name: 'value',
		type: 'string',
		displayOptions: {
			show: {
				resource: ['affiliateMetadata'],
				operation: ['update'],
			},
		},
		default: '',
		description: 'Value to set for the metadata key',
	},
];
