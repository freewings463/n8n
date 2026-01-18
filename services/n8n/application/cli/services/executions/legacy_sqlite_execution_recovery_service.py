"""
MIGRATION-META:
  source_path: packages/cli/src/executions/legacy-sqlite-execution-recovery.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/executions 的执行服务。导入/依赖:外部:assert；内部:@n8n/backend-common、@n8n/config、@n8n/db、@n8n/di；本地:无。导出:LegacySqliteExecutionRecoveryService。关键函数/方法:cleanupWorkflowExecutions、assert。用于封装执行业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/executions/legacy-sqlite-execution-recovery.service.ts -> services/n8n/application/cli/services/executions/legacy_sqlite_execution_recovery_service.py

import { Logger } from '@n8n/backend-common';
import { GlobalConfig } from '@n8n/config';
import { DbConnection, ExecutionRepository } from '@n8n/db';
import { Service } from '@n8n/di';
import assert from 'assert';

/**
 * Service for recovering executions that are missing execution data, this should only happen
 * for sqlite legacy databases.
 */
@Service()
export class LegacySqliteExecutionRecoveryService {
	private readonly logger: Logger;

	constructor(
		logger: Logger,
		private readonly executionRepository: ExecutionRepository,
		private readonly globalConfig: GlobalConfig,
		private readonly dbConnection: DbConnection,
	) {
		this.logger = logger.scoped('legacy-sqlite-execution-recovery');
	}

	/**
	 * Remove workflow executions that are in the `new` state but have no associated execution data.
	 * This is a legacy recovery operation for SQLite databases where executions might be left
	 * in an inconsistent state due to missing execution data.
	 * It marks these executions as `crashed` to prevent them from being processed further.
	 * This method should only be called when we are in legacy SQLite mode.
	 */
	async cleanupWorkflowExecutions() {
		assert(this.globalConfig.database.isLegacySqlite, 'Only usable when on legacy SQLite driver');
		assert(
			this.dbConnection.connectionState.connected && this.dbConnection.connectionState.migrated,
			'The database connection must be connected and migrated before running cleanupWorkflowExecutions',
		);

		this.logger.debug('Starting legacy SQLite execution recovery...');

		const invalidExecutions = await this.executionRepository.findQueuedExecutionsWithoutData();

		if (invalidExecutions.length > 0) {
			await this.executionRepository.markAsCrashed(invalidExecutions.map((e) => e.id));
			this.logger.debug(
				`Marked ${invalidExecutions.length} executions as crashed due to missing execution data.`,
			);
		}

		this.logger.debug('Legacy SQLite execution recovery completed.');
	}
}
