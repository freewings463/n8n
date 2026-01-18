"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/PostBin/BinDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/PostBin 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:binOperations、binFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/PostBin/BinDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/PostBin/BinDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { buildBinAPIURL, transformBinResponse } from './GenericFunctions';

// Operations for the `Bin` resource:
export const binOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['bin'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create bin',
				routing: {
					request: {
						method: 'POST',
						url: '/api/bin',
					},
					output: {
						postReceive: [transformBinResponse],
					},
				},
				action: 'Create a bin',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a bin',
				routing: {
					request: {
						method: 'GET',
					},
					output: {
						postReceive: [transformBinResponse],
					},
					send: {
						preSend: [
							// Parse binId before sending to make sure it's in the right format
							buildBinAPIURL,
						],
					},
				},
				action: 'Get a bin',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete a bin',
				routing: {
					request: {
						method: 'DELETE',
					},
					send: {
						preSend: [
							// Parse binId before sending to make sure it's in the right format
							buildBinAPIURL,
						],
					},
				},
				action: 'Delete a bin',
			},
		],
		default: 'create',
	},
];

// Properties of the `Bin` resource
export const binFields: INodeProperties[] = [
	{
		displayName: 'Bin ID',
		name: 'binId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['bin'],
				operation: ['get', 'delete'],
			},
		},
		description: 'Unique identifier for each bin',
	},
];
