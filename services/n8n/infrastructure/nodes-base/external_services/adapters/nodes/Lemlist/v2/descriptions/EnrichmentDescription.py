"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Lemlist/v2/descriptions/EnrichmentDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Lemlist/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:enrichmentOperations、enrichmentFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Lemlist/v2/descriptions/EnrichmentDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Lemlist/v2/descriptions/EnrichmentDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const enrichmentOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'get',
		options: [
			{
				name: 'Get',
				value: 'get',
				action: 'Fetches a previously completed enrichment',
			},
			{
				name: 'Enrich Lead',
				value: 'enrichLead',
				action: 'Enrich a lead using an email or LinkedIn URL',
			},
			{
				name: 'Enrich Person',
				value: 'enrichPerson',
				action: 'Enrich a person using an email or LinkedIn URL',
			},
		],
		displayOptions: {
			show: {
				resource: ['enrich'],
			},
		},
	},
];

export const enrichmentFields: INodeProperties[] = [
	// ----------------------------------
	//        enrichment: get
	// ----------------------------------
	{
		displayName: 'Enrichment ID',
		name: 'enrichId',
		type: 'string',
		default: '',
		required: true,
		description: 'ID of the enrichment to retrieve',
		displayOptions: {
			show: {
				resource: ['enrich'],
				operation: ['get'],
			},
		},
	},
	// ----------------------------------
	//        enrichment: enrichLead
	// ----------------------------------
	{
		displayName: 'Lead ID',
		name: 'leadId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['enrich'],
				operation: ['enrichLead'],
			},
		},
	},
	{
		displayName: 'Find Email',
		name: 'findEmail',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				resource: ['enrich'],
				operation: ['enrichLead', 'enrichPerson'],
			},
		},
	},
	{
		displayName: 'Verify Email',
		name: 'verifyEmail',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				resource: ['enrich'],
				operation: ['enrichLead', 'enrichPerson'],
			},
		},
	},
	{
		displayName: 'LinkedIn Enrichment',
		name: 'linkedinEnrichment',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				resource: ['enrich'],
				operation: ['enrichLead', 'enrichPerson'],
			},
		},
	},
	{
		displayName: 'Find Phone',
		name: 'findPhone',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				resource: ['enrich'],
				operation: ['enrichLead', 'enrichPerson'],
			},
		},
	},
	// ----------------------------------
	//				enrichment: enrichPerson
	// ----------------------------------
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['enrich'],
				operation: ['enrichPerson'],
			},
		},
		options: [
			{
				displayName: 'Email',
				name: 'email',
				type: 'string',
				placeholder: 'name@email.com',
				default: '',
			},
			{
				displayName: 'First Name',
				name: 'firstName',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Last Name',
				name: 'lastName',
				type: 'string',
				default: '',
			},
			{
				displayName: 'LinkedIn Url',
				name: 'linkedinUrl',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Company Name',
				name: 'companyName',
				type: 'string',
				default: '',
			},
			{
				displayName: 'Company Domain',
				name: 'companyDomain',
				type: 'string',
				default: '',
			},
		],
	},
];
