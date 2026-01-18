"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Postgres/v2/actions/database/deleteTable.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Postgres/v2 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../helpers/utils。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Postgres/v2/actions/database/deleteTable.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Postgres/v2/actions/database/deleteTable_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import type {
	PgpDatabase,
	PostgresNodeOptions,
	QueriesRunner,
	QueryValues,
	QueryWithValues,
} from '../../helpers/interfaces';
import { addWhereClauses, getWhereClauses } from '../../helpers/utils';
import {
	combineConditionsCollection,
	optionsCollection,
	whereFixedCollection,
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
		displayName: 'Restart Sequences',
		name: 'restartSequences',
		type: 'boolean',
		default: false,
		description: 'Whether to reset identity (auto-increment) columns to their initial values',
		displayOptions: {
			show: {
				deleteCommand: ['truncate'],
			},
		},
	},
	{
		...whereFixedCollection,
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
	runQueries: QueriesRunner,
	items: INodeExecutionData[],
	nodeOptions: PostgresNodeOptions,
	_db?: PgpDatabase,
): Promise<INodeExecutionData[]> {
	const queries: QueryWithValues[] = [];

	for (let i = 0; i < items.length; i++) {
		const options = this.getNodeParameter('options', i, {});

		const schema = this.getNodeParameter('schema', i, undefined, {
			extractValue: true,
		}) as string;

		const table = this.getNodeParameter('table', i, undefined, {
			extractValue: true,
		}) as string;

		const deleteCommand = this.getNodeParameter('deleteCommand', i) as string;

		let query = '';
		let values: QueryValues = [schema, table];

		if (deleteCommand === 'drop') {
			const cascade = options.cascade ? ' CASCADE' : '';
			query = `DROP TABLE IF EXISTS $1:name.$2:name${cascade}`;
		}

		if (deleteCommand === 'truncate') {
			const identity = this.getNodeParameter('restartSequences', i, false)
				? ' RESTART IDENTITY'
				: '';
			const cascade = options.cascade ? ' CASCADE' : '';
			query = `TRUNCATE TABLE $1:name.$2:name${identity}${cascade}`;
		}

		if (deleteCommand === 'delete') {
			const whereClauses = getWhereClauses(this, i);

			const combineConditions = this.getNodeParameter('combineConditions', i, 'AND') as string;

			[query, values] = addWhereClauses(
				this.getNode(),
				i,
				'DELETE FROM $1:name.$2:name',
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

	return await runQueries(queries, nodeOptions);
}
