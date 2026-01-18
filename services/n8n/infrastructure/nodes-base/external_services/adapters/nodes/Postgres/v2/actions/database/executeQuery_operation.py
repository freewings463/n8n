"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Postgres/v2/actions/database/executeQuery.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Postgres/v2 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../common.descriptions。导出:description。关键函数/方法:execute、rawReplacements。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Postgres/v2/actions/database/executeQuery.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Postgres/v2/actions/database/executeQuery_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import { getResolvables, updateDisplayOptions } from '@utils/utilities';

import type {
	PgpDatabase,
	PostgresNodeOptions,
	QueriesRunner,
	QueryWithValues,
} from '../../helpers/interfaces';
import {
	evaluateExpression,
	isJSON,
	replaceEmptyStringsByNulls,
	stringToArray,
} from '../../helpers/utils';
import { optionsCollection } from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		displayName: 'Query',
		name: 'query',
		type: 'string',
		default: '',
		placeholder: 'e.g. SELECT id, name FROM product WHERE quantity > $1 AND price <= $2',
		noDataExpression: true,
		required: true,
		description:
			"The SQL query to execute. You can use n8n expressions and $1, $2, $3, etc to refer to the 'Query Parameters' set in options below.",
		typeOptions: {
			editor: 'sqlEditor',
			sqlDialect: 'PostgreSQL',
		},
		hint: 'Consider using query parameters to prevent SQL injection attacks. Add them in the options below',
	},
	optionsCollection,
];

const displayOptions = {
	show: {
		resource: ['database'],
		operation: ['executeQuery'],
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
	const queries: QueryWithValues[] = replaceEmptyStringsByNulls(
		items,
		nodeOptions.replaceEmptyStrings as boolean,
	).map((_, index) => {
		let query = this.getNodeParameter('query', index) as string;

		for (const resolvable of getResolvables(query)) {
			query = query.replace(resolvable, this.evaluateExpression(resolvable, index) as string);
		}

		let values: Array<IDataObject | string> = [];

		let queryReplacement = this.getNodeParameter('options.queryReplacement', index, '');

		if (typeof queryReplacement === 'number') {
			queryReplacement = String(queryReplacement);
		}

		if (typeof queryReplacement === 'string') {
			const node = this.getNode();

			const rawReplacements = (node.parameters.options as IDataObject)?.queryReplacement as string;

			if (rawReplacements) {
				const nodeVersion = nodeOptions.nodeVersion as number;

				if (nodeVersion >= 2.5) {
					const rawValues = rawReplacements.replace(/^=+/, '');
					const resolvables = getResolvables(rawValues);
					if (resolvables.length) {
						for (const resolvable of resolvables) {
							const evaluatedExpression = evaluateExpression(
								this.evaluateExpression(`${resolvable}`, index),
							);
							const evaluatedValues = isJSON(evaluatedExpression)
								? [evaluatedExpression]
								: stringToArray(evaluatedExpression);

							if (evaluatedValues.length) values.push(...evaluatedValues);
						}
					} else {
						values.push(...stringToArray(rawValues));
					}
				} else {
					const rawValues = rawReplacements
						.replace(/^=+/, '')
						.split(',')
						.filter((entry) => entry)
						.map((entry) => entry.trim());

					for (const rawValue of rawValues) {
						const resolvables = getResolvables(rawValue);

						if (resolvables.length) {
							for (const resolvable of resolvables) {
								values.push(this.evaluateExpression(`${resolvable}`, index) as IDataObject);
							}
						} else {
							values.push(rawValue);
						}
					}
				}
			}
		} else {
			if (Array.isArray(queryReplacement)) {
				values = queryReplacement as IDataObject[];
			} else {
				throw new NodeOperationError(
					this.getNode(),
					'Query Parameters must be a string of comma-separated values or an array of values',
					{ itemIndex: index },
				);
			}
		}

		if (!queryReplacement || nodeOptions.treatQueryParametersInSingleQuotesAsText) {
			let nextValueIndex = values.length + 1;
			const literals = query.match(/'\$[0-9]+'/g) ?? [];
			for (const literal of literals) {
				query = query.replace(literal, `$${nextValueIndex}`);
				values.push(literal.replace(/'/g, ''));
				nextValueIndex++;
			}
		}

		return { query, values, options: { partial: true } };
	});

	return await runQueries(queries, nodeOptions);
}
