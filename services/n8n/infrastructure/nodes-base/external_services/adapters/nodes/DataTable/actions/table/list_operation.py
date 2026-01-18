"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DataTable/actions/table/list.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DataTable/actions 的节点。导入/依赖:外部:无；内部:无；本地:../common/constants、../common/utils。导出:FIELD、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DataTable/actions/table/list.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DataTable/actions/table/list_operation.py

import type {
	IDisplayOptions,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
	ListDataTableOptions,
	ListDataTableOptionsSortByKey,
} from 'n8n-workflow';

import { ROWS_LIMIT_DEFAULT } from '../../common/constants';
import { getDataTableAggregateProxy } from '../../common/utils';

export const FIELD = 'list';

const displayOptions: IDisplayOptions = {
	show: {
		resource: ['table'],
		operation: [FIELD],
	},
};

export const description: INodeProperties[] = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: true,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions,
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		default: ROWS_LIMIT_DEFAULT,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
		},
		displayOptions: {
			show: {
				...displayOptions.show,
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		displayOptions,
		options: [
			{
				displayName: 'Filter by Name',
				name: 'filterName',
				type: 'string',
				default: '',
				description: 'Filter data tables by name (case-insensitive)',
			},
			{
				displayName: 'Sort Field',
				name: 'sortField',
				type: 'options',
				default: 'name',
				options: [
					{ name: 'Created', value: 'createdAt' },
					{ name: 'Name', value: 'name' },
					{ name: 'Size', value: 'sizeBytes' },
					{ name: 'Updated', value: 'updatedAt' },
				] satisfies Array<{ name: string; value: ListDataTableOptionsSortByKey }>,
				description: 'Field to sort by',
			},
			{
				displayName: 'Sort Direction',
				name: 'sortDirection',
				type: 'options',
				default: 'asc',
				options: [
					{ name: 'Ascending', value: 'asc' },
					{ name: 'Descending', value: 'desc' },
				],
			},
		],
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const returnAll = this.getNodeParameter('returnAll', index) as boolean;
	const limit = this.getNodeParameter('limit', index, ROWS_LIMIT_DEFAULT) as number;
	const options = this.getNodeParameter('options', index, {}) as {
		filterName?: string;
		sortField?: string;
		sortDirection?: 'asc' | 'desc';
	};

	const aggregateProxy = await getDataTableAggregateProxy(this);

	const queryOptions: ListDataTableOptions = {};

	if (options.sortField && options.sortDirection) {
		queryOptions.sortBy =
			`${options.sortField}:${options.sortDirection}` as ListDataTableOptions['sortBy'];
	}

	if (options.filterName) {
		queryOptions.filter = { name: options.filterName.toLowerCase() };
	}

	const results: INodeExecutionData[] = [];

	if (returnAll) {
		let skip = 0;
		const take = 100;
		let hasMore = true;

		while (hasMore) {
			const response = await aggregateProxy.getManyAndCount({
				...queryOptions,
				skip,
				take,
			});

			for (const table of response.data) {
				results.push({ json: table });
			}

			skip += take;
			hasMore = response.data.length === take && results.length < response.count;
		}
	} else {
		const response = await aggregateProxy.getManyAndCount({
			...queryOptions,
			skip: 0,
			take: limit,
		});

		for (const table of response.data) {
			results.push({ json: table });
		}
	}

	return results;
}
