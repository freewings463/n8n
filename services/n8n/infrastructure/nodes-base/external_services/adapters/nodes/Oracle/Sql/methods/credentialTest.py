"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Oracle/Sql/methods/credentialTest.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Oracle/Sql 的节点。导入/依赖:外部:oracledb；内部:无；本地:../helpers/interfaces、../transport。导出:无。关键函数/方法:oracleDBConnectionTest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Oracle/Sql/methods/credentialTest.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Oracle/Sql/methods/credentialTest.py

import type {
	ICredentialsDecrypted,
	ICredentialTestFunctions,
	INodeCredentialTestResult,
} from 'n8n-workflow';
import type * as oracleDBTypes from 'oracledb';

import type { OracleDBNodeCredentials } from '../helpers/interfaces';
import { configureOracleDB } from '../transport';

export async function oracleDBConnectionTest(
	this: ICredentialTestFunctions,
	credential: ICredentialsDecrypted,
): Promise<INodeCredentialTestResult> {
	const credentials = credential.data as OracleDBNodeCredentials;

	let pool: oracleDBTypes.Pool;

	try {
		pool = await configureOracleDB.call(this, credentials, {});
		const conn = await pool.getConnection();
		await conn.close();
	} catch (error) {
		const message = error instanceof Error ? error.message : String(error);
		return {
			status: 'Error',
			message,
		};
	}
	return {
		status: 'OK',
		message: 'Connection successful!',
	};
}
