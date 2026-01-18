"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/descriptions/common.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/AzureCosmosDb 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/constants、../helpers/utils。导出:containerResourceLocator、itemResourceLocator、paginationParameters。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/descriptions/common.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/AzureCosmosDb/descriptions/common.py

import type { INodeProperties } from 'n8n-workflow';

import { HeaderConstants } from '../helpers/constants';
import { untilContainerSelected } from '../helpers/utils';

export const containerResourceLocator: INodeProperties = {
	displayName: 'Container',
	name: 'container',
	default: {
		mode: 'list',
		value: '',
	},
	modes: [
		{
			displayName: 'From list',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'searchContainers',
				searchable: true,
			},
		},
		{
			displayName: 'By ID',
			name: 'id',
			hint: 'Enter the container ID',
			placeholder: 'e.g. AndersenFamily',
			type: 'string',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: '^[\\w+=,.@-]+$',
						errorMessage: 'The container ID must follow the allowed pattern',
					},
				},
			],
		},
	],
	required: true,
	type: 'resourceLocator',
};

export const itemResourceLocator: INodeProperties = {
	displayName: 'Item',
	name: 'item',
	default: {
		mode: 'list',
		value: '',
	},
	displayOptions: {
		hide: {
			...untilContainerSelected,
		},
	},
	modes: [
		{
			displayName: 'From list',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'searchItems',
				searchable: true,
			},
		},
		{
			displayName: 'By ID',
			name: 'id',
			hint: 'Enter the item ID',
			placeholder: 'e.g. AndersenFamily',
			type: 'string',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: '^[\\w+=,.@-]+$',
						errorMessage: 'The item ID must follow the allowed pattern',
					},
				},
			],
		},
	],
	required: true,
	type: 'resourceLocator',
};

export const paginationParameters: INodeProperties[] = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		routing: {
			send: {
				paginate: '={{ $value }}',
			},
			operations: {
				pagination: {
					type: 'generic',
					properties: {
						continue: `={{ !!$response.headers?.["${HeaderConstants.X_MS_CONTINUATION}"] }}`,
						request: {
							headers: {
								[HeaderConstants.X_MS_CONTINUATION]: `={{ $response.headers?.["${HeaderConstants.X_MS_CONTINUATION}"] }}`,
							},
						},
					},
				},
			},
		},
		type: 'boolean',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		default: 50,
		description: 'Max number of results to return',
		displayOptions: {
			show: {
				returnAll: [false],
			},
		},
		routing: {
			request: {
				headers: {
					[HeaderConstants.X_MS_MAX_ITEM_COUNT]: '={{ $value || undefined }}',
				},
			},
		},
		type: 'number',
		typeOptions: {
			minValue: 1,
		},
		validateType: 'number',
	},
];
