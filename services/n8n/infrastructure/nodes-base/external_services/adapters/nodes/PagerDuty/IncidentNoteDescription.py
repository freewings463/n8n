"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/PagerDuty/IncidentNoteDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/PagerDuty 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:incidentNoteOperations、incidentNoteFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/PagerDuty/IncidentNoteDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/PagerDuty/IncidentNoteDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const incidentNoteOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['incidentNote'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a incident note',
				action: 'Create an incident note',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: "Get many incident's notes",
				action: 'Get many incident notes',
			},
		],
		default: 'create',
	},
];

export const incidentNoteFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                incidentNote:create                         */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Incident ID',
		name: 'incidentId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['incidentNote'],
				operation: ['create'],
			},
		},
		description: 'Unique identifier for the incident',
	},
	{
		displayName: 'Content',
		name: 'content',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['incidentNote'],
				operation: ['create'],
			},
		},
		description: 'The note content',
	},
	{
		displayName: 'Email',
		name: 'email',
		type: 'string',
		placeholder: 'name@email.com',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['incidentNote'],
				operation: ['create'],
			},
		},
		description: 'The email address of a valid user associated with the account making the request',
	},
	/* -------------------------------------------------------------------------- */
	/*                                 incidentNote:getAll                        */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Incident ID',
		name: 'incidentId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['incidentNote'],
				operation: ['getAll'],
			},
		},
		description: 'Unique identifier for the incident',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['incidentNote'],
			},
		},
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['incidentNote'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 500,
		},
		default: 100,
		description: 'Max number of results to return',
	},
];
