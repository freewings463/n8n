"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Postgres/v2/methods/credentialTest.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Postgres/v2 的节点。导入/依赖:外部:无；内部:无；本地:../../transport、../helpers/interfaces。导出:无。关键函数/方法:postgresConnectionTest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Postgres/v2/methods/credentialTest.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Postgres/v2/methods/credentialTest.py

import type {
	ICredentialsDecrypted,
	ICredentialTestFunctions,
	INodeCredentialTestResult,
} from 'n8n-workflow';

import { configurePostgres } from '../../transport';
import type { PgpConnection, PostgresNodeCredentials } from '../helpers/interfaces';

export async function postgresConnectionTest(
	this: ICredentialTestFunctions,
	credential: ICredentialsDecrypted,
): Promise<INodeCredentialTestResult> {
	const credentials = credential.data as PostgresNodeCredentials;

	let connection: PgpConnection | undefined;

	try {
		const { db } = await configurePostgres.call(this, credentials, {});

		connection = await db.connect();
	} catch (error) {
		let message = error.message as string;

		if (error.message.includes('ECONNREFUSED')) {
			message = 'Connection refused';
		}

		if (error.message.includes('ENOTFOUND')) {
			message = 'Host not found, please check your host name';
		}

		if (error.message.includes('ETIMEDOUT')) {
			message = 'Connection timed out';
		}

		return {
			status: 'Error',
			message,
		};
	} finally {
		if (connection) {
			await connection.done();
		}
	}
	return {
		status: 'OK',
		message: 'Connection successful!',
	};
}
