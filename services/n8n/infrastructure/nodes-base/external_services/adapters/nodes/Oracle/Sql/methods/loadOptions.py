"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Oracle/Sql/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Oracle/Sql 的节点。导入/依赖:外部:oracledb；内部:n8n-workflow；本地:../helpers/interfaces、../helpers/utils、../transport。导出:无。关键函数/方法:getColumns、getColumnsMultiOptions。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Oracle/Sql/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Oracle/Sql/methods/loadOptions.py

import type { ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';
import type * as oracleDBTypes from 'oracledb';

import type { OracleDBNodeCredentials } from '../helpers/interfaces';
import { getColumnMetaData } from '../helpers/utils';
import { configureOracleDB } from '../transport';

export async function getColumns(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const credentials = await this.getCredentials<OracleDBNodeCredentials>('oracleDBApi');
	const options = { nodeVersion: this.getNode().typeVersion };

	const pool: oracleDBTypes.Pool = await configureOracleDB.call(this, credentials, options);

	const schema = this.getNodeParameter('schema', 0, {
		extractValue: true,
	}) as string;

	const table = this.getNodeParameter('table', 0, {
		extractValue: true,
	}) as string;

	const columns = await getColumnMetaData(this.getNode(), pool, schema, table);

	return columns.map((column) => ({
		name: column.columnName,
		value: column.columnName,
		description: `Type: ${column.dataType.toUpperCase()}, Nullable: ${column.isNullable}`,
	}));
}

export async function getColumnsMultiOptions(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData = await getColumns.call(this);
	const returnAll = { name: '*', value: '*', description: 'All columns' };
	return [returnAll, ...returnData];
}
