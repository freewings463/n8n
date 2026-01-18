"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/descriptions/item/Item.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/AzureCosmosDb 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./delete.operation、./get.operation、./getAll.operation 等5项。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/descriptions/item/Item.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/AzureCosmosDb/descriptions/item/Item_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as del from './delete.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';
import * as query from './query.operation';
import * as update from './update.operation';
import { HeaderConstants } from '../../helpers/constants';
import { handleError } from '../../helpers/errorHandler';
import { simplifyData, validatePartitionKey } from '../../helpers/utils';

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['item'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new item',
				routing: {
					send: {
						preSend: [validatePartitionKey],
					},
					request: {
						method: 'POST',
						url: '=/colls/{{ $parameter["container"] }}/docs',
						headers: {
							[HeaderConstants.X_MS_DOCUMENTDB_IS_UPSERT]: 'True',
						},
					},
					output: {
						postReceive: [handleError],
					},
				},
				action: 'Create item',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete an existing item',
				routing: {
					send: {
						preSend: [validatePartitionKey],
					},
					request: {
						method: 'DELETE',
						url: '=/colls/{{ $parameter["container"] }}/docs/{{ $parameter["item"] }}',
					},
					output: {
						postReceive: [
							handleError,
							{
								type: 'set',
								properties: {
									value: '={{ { "deleted": true } }}',
								},
							},
						],
					},
				},
				action: 'Delete item',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve an item',
				routing: {
					send: {
						preSend: [validatePartitionKey],
					},
					request: {
						method: 'GET',
						url: '=/colls/{{ $parameter["container"]}}/docs/{{$parameter["item"]}}',
						headers: {
							[HeaderConstants.X_MS_DOCUMENTDB_IS_UPSERT]: 'True',
						},
					},
					output: {
						postReceive: [handleError, simplifyData],
					},
				},
				action: 'Get item',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve a list of items',
				routing: {
					request: {
						method: 'GET',
						url: '=/colls/{{ $parameter["container"] }}/docs',
					},
					output: {
						postReceive: [
							handleError,
							{
								type: 'rootProperty',
								properties: {
									property: 'Documents',
								},
							},
							simplifyData,
						],
					},
				},
				action: 'Get many items',
			},
			{
				name: 'Execute Query',
				value: 'query',
				routing: {
					request: {
						method: 'POST',
						url: '=/colls/{{ $parameter["container"] }}/docs',
						headers: {
							'Content-Type': 'application/query+json',
							'x-ms-documentdb-isquery': 'True',
							'x-ms-documentdb-query-enablecrosspartition': 'True',
						},
					},
					output: {
						postReceive: [
							handleError,
							{
								type: 'rootProperty',
								properties: {
									property: 'Documents',
								},
							},
							simplifyData,
						],
					},
				},
				action: 'Query items',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update an existing item',
				routing: {
					send: {
						preSend: [validatePartitionKey],
					},
					request: {
						method: 'PUT',
						url: '=/colls/{{ $parameter["container"] }}/docs/{{ $parameter["item"] }}',
						headers: {
							'Content-Type': 'application/json-patch+json',
						},
					},
					output: {
						postReceive: [handleError],
					},
				},
				action: 'Update item',
			},
		],
		default: 'getAll',
	},

	...create.description,
	...del.description,
	...get.description,
	...getAll.description,
	...query.description,
	...update.description,
];
