"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Postgres/v2/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Postgres/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport、../helpers/interfaces、../helpers/utils。导出:无。关键函数/方法:getColumns、getColumnsMultiOptions、getColumnsWithoutColumnToMatchOn。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Postgres/v2/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Postgres/v2/methods/loadOptions.py

import type { ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

import { configurePostgres } from '../../transport';
import type { PostgresNodeCredentials } from '../helpers/interfaces';
import { getTableSchema } from '../helpers/utils';

export async function getColumns(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const credentials = await this.getCredentials<PostgresNodeCredentials>('postgres');
	const options = { nodeVersion: this.getNode().typeVersion };

	const { db } = await configurePostgres.call(this, credentials, options);

	const schema = this.getNodeParameter('schema', 0, {
		extractValue: true,
	}) as string;

	const table = this.getNodeParameter('table', 0, {
		extractValue: true,
	}) as string;

	const columns = await getTableSchema(db, schema, table);

	return columns.map((column) => ({
		name: column.column_name,
		value: column.column_name,
		description: `Type: ${column.data_type.toUpperCase()}, Nullable: ${column.is_nullable}`,
	}));
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
