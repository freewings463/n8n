"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Oracle/Sql/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Oracle/Sql 的节点。导入/依赖:外部:oracledb；内部:n8n-workflow；本地:../helpers/interfaces、../transport。导出:无。关键函数/方法:schemaSearch、tableSearch。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Oracle/Sql/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Oracle/Sql/methods/listSearch.py

import { NodeOperationError } from 'n8n-workflow';
import type { ILoadOptionsFunctions, INodeListSearchResult } from 'n8n-workflow';
import * as oracleDBTypes from 'oracledb';

import type { OracleDBNodeCredentials } from '../helpers/interfaces';
import { configureOracleDB } from '../transport';

export async function schemaSearch(this: ILoadOptionsFunctions): Promise<INodeListSearchResult> {
	const credentials = await this.getCredentials<OracleDBNodeCredentials>('oracleDBApi');
	const options = { nodeVersion: this.getNode().typeVersion };

	const pool: oracleDBTypes.Pool = await configureOracleDB.call(this, credentials, options);

	let conn: oracleDBTypes.Connection | undefined;

	try {
		conn = await pool.getConnection();

		const response = await conn.execute<{ USERNAME: string }>(
			'SELECT username FROM all_users',
			[],
			{
				outFormat: oracleDBTypes.OUT_FORMAT_OBJECT,
			},
		);

		const results =
			response.rows?.map((schema) => ({
				name: schema.USERNAME,
				value: schema.USERNAME,
			})) ?? [];

		return { results };
	} catch (error) {
		throw new NodeOperationError(this.getNode(), `Failed to fetch schemas: ${error.message}`);
	} finally {
		if (conn) {
			await conn.close(); // Ensure connection is closed
		}
	}
}

export async function tableSearch(this: ILoadOptionsFunctions): Promise<INodeListSearchResult> {
	const credentials = await this.getCredentials<OracleDBNodeCredentials>('oracleDBApi');
	const options = { nodeVersion: this.getNode().typeVersion };

	const pool: oracleDBTypes.Pool = await configureOracleDB.call(this, credentials, options);

	let conn: oracleDBTypes.Connection | undefined;

	try {
		// Get the connection from the pool
		conn = await pool.getConnection();

		// Retrieve the schema parameter
		const schema = this.getNodeParameter('schema', 0, {
			extractValue: true,
		}) as string;

		// Execute the SQL query to fetch table names for the given schema
		const response = await conn.execute<{ TABLE_NAME: string }>(
			'SELECT table_name FROM all_tables WHERE owner = (:1)',
			[schema],
			{
				outFormat: oracleDBTypes.OUT_FORMAT_OBJECT, // Ensure that the response is in object format
			},
		);

		// Map through the response.rows and format them
		const results =
			response.rows?.map((table) => ({
				name: table.TABLE_NAME,
				value: table.TABLE_NAME,
			})) ?? []; // Handle the case where rows might be undefined or empty

		// Return the results in the required format
		return { results };
	} catch (error) {
		throw new NodeOperationError(this.getNode(), `Failed to fetch tables: ${error.message}`);
	} finally {
		// Ensure the connection is always closed
		if (conn) {
			await conn.close();
		}
	}
}
