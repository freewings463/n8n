"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/connection/db-connection.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/db/src/connection 的模块。导入/依赖:外部:timers/promises；内部:@n8n/backend-common、@n8n/config、@n8n/constants、@n8n/decorators、@n8n/di、@n8n/typeorm 等2项；本地:./db-connection-options、../migrations/migration-helpers、../migrations/migration-types。导出:DbConnection。关键函数/方法:init、migrate、close、clearTimeout、scheduleNextPing、async、ping、setTimeoutP。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/connection/db-connection.ts -> services/n8n/application/n8n-db/services/connection/db_connection.py

import { inTest, Logger } from '@n8n/backend-common';
import { DatabaseConfig } from '@n8n/config';
import { Time } from '@n8n/constants';
import { Memoized } from '@n8n/decorators';
import { Container, Service } from '@n8n/di';
import { DataSource } from '@n8n/typeorm';
import { BinaryDataConfig, ErrorReporter } from 'n8n-core';
import { DbConnectionTimeoutError, ensureError, OperationalError } from 'n8n-workflow';
import { setTimeout as setTimeoutP } from 'timers/promises';

import { DbConnectionOptions } from './db-connection-options';
import { wrapMigration } from '../migrations/migration-helpers';
import type { Migration } from '../migrations/migration-types';

type ConnectionState = {
	connected: boolean;
	migrated: boolean;
};

@Service()
export class DbConnection {
	private dataSource: DataSource;

	private pingTimer: NodeJS.Timeout | undefined;

	readonly connectionState: ConnectionState = {
		connected: false,
		migrated: false,
	};

	constructor(
		private readonly errorReporter: ErrorReporter,
		private readonly connectionOptions: DbConnectionOptions,
		private readonly databaseConfig: DatabaseConfig,
		private readonly logger: Logger,
		private readonly binaryDataConfig: BinaryDataConfig,
	) {
		this.dataSource = new DataSource(this.options);
		Container.set(DataSource, this.dataSource);
	}

	@Memoized
	get options() {
		return this.connectionOptions.getOptions();
	}

	async init(): Promise<void> {
		const { connectionState, options } = this;
		if (connectionState.connected) return;
		try {
			await this.dataSource.initialize();
		} catch (e) {
			let error = ensureError(e);
			if (
				options.type === 'postgres' &&
				error.message === 'Connection terminated due to connection timeout'
			) {
				error = new DbConnectionTimeoutError({
					cause: error,
					configuredTimeoutInMs: options.connectTimeoutMS!,
				});
			}
			throw error;
		}

		if (
			(options.type === 'mysql' || options.type === 'mariadb') &&
			this.binaryDataConfig.availableModes.includes('database')
		) {
			const maxAllowedPacket = this.binaryDataConfig.dbMaxFileSize * 1024 * 1024;
			try {
				await this.dataSource.query(`SET GLOBAL max_allowed_packet = ${maxAllowedPacket}`);
			} catch {
				this.logger.warn(
					`Failed to set \`max_allowed_packet\` to ${maxAllowedPacket} bytes on your MySQL server. ` +
						`Please set \`max_allowed_packet\` to at least ${this.binaryDataConfig.dbMaxFileSize} MiB in your MySQL server configuration.`,
				);
			}
		}

		connectionState.connected = true;
		if (!inTest) this.scheduleNextPing();
	}

	async migrate() {
		const { dataSource, connectionState } = this;
		(dataSource.options.migrations as Migration[]).forEach(wrapMigration);
		await dataSource.runMigrations({ transaction: 'each' });
		connectionState.migrated = true;
	}

	async close() {
		if (this.pingTimer) {
			clearTimeout(this.pingTimer);
			this.pingTimer = undefined;
		}

		if (this.dataSource.isInitialized) {
			await this.dataSource.destroy();
			this.connectionState.connected = false;
		}
	}

	/** Ping DB connection every `pingIntervalSeconds` seconds to check if it is still alive. */
	private scheduleNextPing() {
		this.pingTimer = setTimeout(
			async () => await this.ping(),
			this.databaseConfig.pingIntervalSeconds * Time.seconds.toMilliseconds,
		);
	}

	private async ping() {
		if (!this.dataSource.isInitialized) return;
		const abortController = new AbortController();

		try {
			await Promise.race([
				this.dataSource.query('SELECT 1'),
				setTimeoutP(5000, undefined, { signal: abortController.signal }).then(() => {
					throw new OperationalError('Database connection timed out');
				}),
			]);

			if (!this.connectionState.connected) {
				this.logger.info('Database connection recovered');
			}

			this.connectionState.connected = true;
			return;
		} catch (error) {
			this.connectionState.connected = false;
			if (error instanceof OperationalError) {
				this.logger.warn(error.message);
			} else {
				this.errorReporter.error(error);
			}
		} finally {
			abortController.abort();
			this.scheduleNextPing();
		}
	}
}
