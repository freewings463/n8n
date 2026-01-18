"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MySql/v2/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MySql/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/interfaces、../transport。导出:无。关键函数/方法:searchTables、response、results。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MySql/v2/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MySql/v2/methods/listSearch.py

import type { IDataObject, ILoadOptionsFunctions, INodeListSearchResult } from 'n8n-workflow';

import type { MysqlNodeCredentials } from '../helpers/interfaces';
import { createPool } from '../transport';

export async function searchTables(this: ILoadOptionsFunctions): Promise<INodeListSearchResult> {
	const credentials = await this.getCredentials<MysqlNodeCredentials>('mySql');

	const nodeOptions = this.getNodeParameter('options', 0) as IDataObject;

	const pool = await createPool.call(this, credentials, nodeOptions);

	try {
		const connection = await pool.getConnection();

		const query = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = ?';
		const values = [credentials.database];

		const formatedQuery = connection.format(query, values);

		const response = (await connection.query(formatedQuery))[0];

		connection.release();

		const results = (response as IDataObject[]).map((table) => ({
			name: (table.table_name as string) || (table.TABLE_NAME as string),
			value: (table.table_name as string) || (table.TABLE_NAME as string),
		}));

		return { results };
	} finally {
		await pool.end();
	}
}
