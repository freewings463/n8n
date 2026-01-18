"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MySql/v1/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MySql/v1 的节点。导入/依赖:外部:mysql2/promise；内部:无；本地:无。导出:无。关键函数/方法:createConnection、searchTables、results。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MySql/v1/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MySql/v1/GenericFunctions.py

import mysql2 from 'mysql2/promise';
import type {
	ICredentialDataDecryptedObject,
	IDataObject,
	ILoadOptionsFunctions,
	INodeListSearchResult,
} from 'n8n-workflow';

export async function createConnection(
	credentials: ICredentialDataDecryptedObject,
): Promise<mysql2.Connection> {
	const { ssl, caCertificate, clientCertificate, clientPrivateKey, ...baseCredentials } =
		credentials;

	if (ssl) {
		baseCredentials.ssl = {};

		if (caCertificate) {
			baseCredentials.ssl.ca = caCertificate;
		}

		if (clientCertificate || clientPrivateKey) {
			baseCredentials.ssl.cert = clientCertificate;
			baseCredentials.ssl.key = clientPrivateKey;
		}
	}

	return await mysql2.createConnection(baseCredentials);
}

export async function searchTables(
	this: ILoadOptionsFunctions,
	tableName?: string,
): Promise<INodeListSearchResult> {
	const credentials = await this.getCredentials('mySql');
	const connection = await createConnection(credentials);
	const sql = `SELECT table_name
FROM   information_schema.tables
WHERE  table_schema = ?
AND table_name LIKE ?
ORDER  BY table_name`;

	const values = [credentials.database, `%${tableName ?? ''}%`];
	const [rows] = await connection.query(sql, values);
	const results = (rows as IDataObject[]).map((table) => ({
		name: (table.table_name as string) || (table.TABLE_NAME as string),
		value: (table.table_name as string) || (table.TABLE_NAME as string),
	}));
	await connection.end();
	return { results };
}
