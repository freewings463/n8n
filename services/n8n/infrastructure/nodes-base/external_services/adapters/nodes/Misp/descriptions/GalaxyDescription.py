"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Misp/descriptions/GalaxyDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Misp/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:galaxyOperations、galaxyFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Misp/descriptions/GalaxyDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Misp/descriptions/GalaxyDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const galaxyOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		displayOptions: {
			show: {
				resource: ['galaxy'],
			},
		},
		noDataExpression: true,
		options: [
			{
				name: 'Delete',
				value: 'delete',
				action: 'Delete a galaxy',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a galaxy',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many galaxies',
			},
		],
		default: 'get',
	},
];

export const galaxyFields: INodeProperties[] = [
	// ----------------------------------------
	//              galaxy: delete
	// ----------------------------------------
	{
		displayName: 'Galaxy ID',
		name: 'galaxyId',
		description: 'UUID or numeric ID of the galaxy',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['galaxy'],
				operation: ['delete'],
			},
		},
	},

	// ----------------------------------------
	//               galaxy: get
	// ----------------------------------------
	{
		displayName: 'Galaxy ID',
		name: 'galaxyId',
		description: 'UUID or numeric ID of the galaxy',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['galaxy'],
				operation: ['get'],
			},
		},
	},

	// ----------------------------------------
	//              galaxy: getAll
	// ----------------------------------------
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['galaxy'],
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
				resource: ['galaxy'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
];
