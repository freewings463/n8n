"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Chat/descriptions/MediaDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Chat 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:mediaOperations、mediaFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Chat/descriptions/MediaDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Chat/descriptions/MediaDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const mediaOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		noDataExpression: true,
		type: 'options',
		displayOptions: {
			show: {
				resource: ['media'],
			},
		},
		options: [
			{
				name: 'Download',
				value: 'download',
				description: 'Download media',
				action: 'Download media',
			},
		],
		default: 'download',
	},
];

export const mediaFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 media:download                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Resource Name',
		name: 'resourceName',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['media'],
				operation: ['download'],
			},
		},
		default: '',
		description: 'Name of the media that is being downloaded',
	},
	{
		displayName: 'Put Output File in Field',
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		required: true,
		displayOptions: {
			show: {
				resource: ['media'],
				operation: ['download'],
			},
		},
		hint: 'The name of the output binary field to put the file in',
	},
];
