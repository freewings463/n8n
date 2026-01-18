"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MySql/v2/actions/database/deleteTable.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MySql/v2 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../helpers/interfaces、../helpers/utils。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MySql/v2/actions/database/deleteTable.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MySql/v2/actions/database/deleteTable_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import type { QueryRunner, QueryValues, QueryWithValues } from '../../helpers/interfaces';
import { addWhereClauses, escapeSqlIdentifier, getWhereClauses } from '../../helpers/utils';
import {
	optionsCollection,
	selectRowsFixedCollection,
	combineConditionsCollection,
} from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		displayName: 'Command',
		name: 'deleteCommand',
		type: 'options',
		default: 'truncate',
		options: [
			{
				name: 'Truncate',
				value: 'truncate',
				description: "Only removes the table's data and preserves the table's structure",
			},
			{
				name: 'Delete',
				value: 'delete',
				description:
					"Delete the rows that match the 'Select Rows' conditions below. If no selection is made, all rows in the table are deleted.",
			},
			{
				name: 'Drop',
				value: 'drop',
				description: "Deletes the table's data and also the table's structure permanently",
			},
		],
	},
	{
		...selectRowsFixedCollection,
		displayOptions: {
			show: {
				deleteCommand: ['delete'],
			},
		},
	},
	{
		...combineConditionsCollection,
		displayOptions: {
			show: {
				deleteCommand: ['delete'],
			},
		},
	},
	optionsCollection,
];

const displayOptions = {
	show: {
		resource: ['database'],
		operation: ['deleteTable'],
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

		const deleteCommand = this.getNodeParameter('deleteCommand', i) as string;

		let query = '';
		let values: QueryValues = [];

		if (deleteCommand === 'drop') {
			query = `DROP TABLE IF EXISTS ${escapeSqlIdentifier(table)}`;
		}

		if (deleteCommand === 'truncate') {
			query = `TRUNCATE TABLE ${escapeSqlIdentifier(table)}`;
		}

		if (deleteCommand === 'delete') {
			const whereClauses = getWhereClauses(this, i);

			const combineConditions = this.getNodeParameter('combineConditions', i, 'AND') as string;

			[query, values] = addWhereClauses(
				this.getNode(),
				i,
				`DELETE FROM ${escapeSqlIdentifier(table)}`,
				whereClauses,
				values,
				combineConditions,
			);
		}

		if (query === '') {
			throw new NodeOperationError(
				this.getNode(),
				'Invalid delete command, only drop, delete and truncate are supported ',
				{ itemIndex: i },
			);
		}

		const queryWithValues = { query, values };

		queries.push(queryWithValues);
	}

	returnData = await runQueries(queries);

	return returnData;
}
