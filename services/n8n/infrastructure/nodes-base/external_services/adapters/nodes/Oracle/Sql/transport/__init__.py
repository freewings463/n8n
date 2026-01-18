"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Oracle/Sql/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Oracle/Sql 的入口。导入/依赖:外部:oracledb、@utils/connection-pool-manager；内部:无；本地:../helpers/interfaces。导出:无。关键函数/方法:getOracleDBConfig、configureOracleDB、fallBackHandler。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Oracle/Sql/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Oracle/Sql/transport/__init__.py

import type {
	IExecuteFunctions,
	ICredentialTestFunctions,
	ILoadOptionsFunctions,
	ITriggerFunctions,
} from 'n8n-workflow';
import oracledb from 'oracledb';

import { ConnectionPoolManager } from '@utils/connection-pool-manager';

import type { OracleDBNodeOptions, OracleDBNodeCredentials } from '../helpers/interfaces';

// used for thick mode to call initOracleClient API only once.
let initializeDriverMode = false;

const getOracleDBConfig = (credentials: OracleDBNodeCredentials) => {
	const { useThickMode, useSSL, ...dbConfig } = {
		...credentials,
		privilege: credentials.privilege || undefined,
	};

	return dbConfig;
};

export async function configureOracleDB(
	this: IExecuteFunctions | ICredentialTestFunctions | ILoadOptionsFunctions | ITriggerFunctions,
	credentials: OracleDBNodeCredentials,
	options: OracleDBNodeOptions = {},
): Promise<oracledb.Pool> {
	const poolManager = ConnectionPoolManager.getInstance(this.logger);
	const fallBackHandler = async (abortController: AbortController): Promise<oracledb.Pool> => {
		const dbConfig = getOracleDBConfig(credentials);

		if (credentials.useThickMode) {
			if (!initializeDriverMode) {
				oracledb.initOracleClient();
				initializeDriverMode = true;
			}
		} else if (initializeDriverMode) {
			// Thick mode is initialized, cannot switch back to thin mode
			throw new Error('Thin mode can not be used after thick mode initialization');
		}
		const pool = await oracledb.createPool(dbConfig);

		abortController.signal.addEventListener('abort', async () => {
			try {
				await pool.close();
				this.logger.debug('pool closed on abort');
			} catch (error) {
				this.logger.error('Error closing pool on abort', { error });
			}
		});
		return pool;
	};

	return await poolManager.getConnection<oracledb.Pool>({
		credentials,
		nodeType: 'oracledb',
		nodeVersion: String(options.nodeVersion ?? '1'),
		fallBackHandler,
		wasUsed: (pool) => {
			if (pool) {
				this.logger.debug(`DB pool reused, open connections: ${pool.connectionsOpen}`);
			}
		},
	});
}
