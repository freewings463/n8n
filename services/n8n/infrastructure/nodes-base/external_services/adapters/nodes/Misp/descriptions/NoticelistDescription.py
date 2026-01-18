"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Misp/descriptions/NoticelistDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Misp/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:noticelistOperations、noticelistFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Misp/descriptions/NoticelistDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Misp/descriptions/NoticelistDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const noticelistOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		displayOptions: {
			show: {
				resource: ['noticelist'],
			},
		},
		noDataExpression: true,
		options: [
			{
				name: 'Get',
				value: 'get',
				action: 'Get a noticelist',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get many noticelists',
			},
		],
		default: 'get',
	},
];

export const noticelistFields: INodeProperties[] = [
	// ----------------------------------------
	//             noticelist: get
	// ----------------------------------------
	{
		displayName: 'Noticelist ID',
		name: 'noticelistId',
		description: 'Numeric ID of the noticelist',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['noticelist'],
				operation: ['get'],
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
				resource: ['noticelist'],
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
				resource: ['noticelist'],
				operation: ['getAll'],
				returnAll: [false],
			},
		},
	},
];
