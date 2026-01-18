"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MySql/v2/actions/database/select.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MySql/v2 的节点。导入/依赖:外部:@utils/utilities；内部:无；本地:../helpers/interfaces。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MySql/v2/actions/database/select.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MySql/v2/actions/database/select_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import type { QueryRunner, QueryValues, QueryWithValues, SortRule } from '../../helpers/interfaces';
import {
	addSortRules,
	addWhereClauses,
	escapeSqlIdentifier,
	getWhereClauses,
} from '../../helpers/utils';
import {
	optionsCollection,
	sortFixedCollection,
	selectRowsFixedCollection,
	combineConditionsCollection,
} from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions: {
			show: {
				resource: ['event'],
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
				returnAll: [false],
			},
		},
	},
	selectRowsFixedCollection,
	combineConditionsCollection,
	sortFixedCollection,
	optionsCollection,
];

const displayOptions = {
	show: {
		resource: ['database'],
		operation: ['select'],
	},
	hide: {
		table: [''],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	inputItems: INodeExecutionData[],
	runQueries: QueryRunner,
): Promise<INodeExecutionData[]> {
	let returnData: INodeExecutionData[] = [];

	const queries: QueryWithValues[] = [];

	for (let i = 0; i < inputItems.length; i++) {
		const table = this.getNodeParameter('table', i, undefined, {
			extractValue: true,
		}) as string;

		const outputColumns = this.getNodeParameter('options.outputColumns', i, ['*']) as string[];
		const selectDistinct = this.getNodeParameter('options.selectDistinct', i, false) as boolean;

		let query = '';
		const SELECT = selectDistinct ? 'SELECT DISTINCT' : 'SELECT';

		if (outputColumns.includes('*')) {
			query = `${SELECT} * FROM ${escapeSqlIdentifier(table)}`;
		} else {
			const escapedColumns = outputColumns.map(escapeSqlIdentifier).join(', ');
			query = `${SELECT} ${escapedColumns} FROM ${escapeSqlIdentifier(table)}`;
		}

		let values: QueryValues = [];

		const whereClauses = getWhereClauses(this, i);

		const combineConditions = this.getNodeParameter('combineConditions', i, 'AND') as string;

		[query, values] = addWhereClauses(
			this.getNode(),
			i,
			query,
			whereClauses,
			values,
			combineConditions,
		);

		const sortRules =
			((this.getNodeParameter('sort', i, []) as IDataObject).values as SortRule[]) || [];

		[query, values] = addSortRules(query, sortRules, values);

		const returnAll = this.getNodeParameter('returnAll', i, false);
		if (!returnAll) {
			const limit = this.getNodeParameter('limit', i, 50);
			query += ' LIMIT ?';
			values.push(limit);
		}

		queries.push({ query, values });
	}

	returnData = await runQueries(queries);

	return returnData;
}
