"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MySql/v2/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MySql/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/interfaces、../helpers/utils、../transport。导出:无。关键函数/方法:getColumns、columns、getColumnsMultiOptions、getColumnsWithoutColumnToMatchOn。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MySql/v2/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MySql/v2/methods/loadOptions.py

import type { IDataObject, ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

import type { MysqlNodeCredentials } from '../helpers/interfaces';
import { escapeSqlIdentifier } from '../helpers/utils';
import { createPool } from '../transport';

export async function getColumns(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const credentials = await this.getCredentials<MysqlNodeCredentials>('mySql');
	const nodeOptions = this.getNodeParameter('options', 0) as IDataObject;

	const pool = await createPool.call(this, credentials, nodeOptions);

	try {
		const connection = await pool.getConnection();

		const table = this.getNodeParameter('table', 0, {
			extractValue: true,
		}) as string;

		const columns = (
			await connection.query(
				`SHOW COLUMNS FROM ${escapeSqlIdentifier(table)} FROM ${escapeSqlIdentifier(
					credentials.database,
				)}`,
			)
		)[0] as IDataObject[];

		connection.release();

		return (columns || []).map((column: IDataObject) => ({
			name: column.Field as string,
			value: column.Field as string,
			// eslint-disable-next-line n8n-nodes-base/node-param-description-lowercase-first-char
			description: `type: ${(column.Type as string).toUpperCase()}, nullable: ${
				column.Null as string
			}`,
		}));
	} finally {
		await pool.end();
	}
}

export async function getColumnsMultiOptions(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData = await getColumns.call(this);
	const returnAll = { name: '*', value: '*', description: 'All columns' };
	return [returnAll, ...returnData];
}

export async function getColumnsWithoutColumnToMatchOn(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const columnToMatchOn = this.getNodeParameter('columnToMatchOn') as string;
	const returnData = await getColumns.call(this);
	return returnData.filter((column) => column.value !== columnToMatchOn);
}
