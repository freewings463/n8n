"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/connection/db-connection-options.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/db/src/connection 的模块。导入/依赖:外部:node:tls；内部:@n8n/backend-common、@n8n/config、@n8n/di、@n8n/typeorm 等5项；本地:../entities、../migrations/mysqldb、../migrations/postgresdb、../migrations/sqlite 等1项。导出:DbConnectionOptions。关键函数/方法:getOverrides、getOptions、getCommonOptions、getSqliteConnectionOptions、getPostgresConnectionOptions、getMysqlConnectionOptions。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/connection/db-connection-options.ts -> services/n8n/application/n8n-db/services/connection/db_connection_options.py

import { ModuleRegistry } from '@n8n/backend-common';
import { DatabaseConfig, InstanceSettingsConfig } from '@n8n/config';
import { Service } from '@n8n/di';
import type { DataSourceOptions, LoggerOptions } from '@n8n/typeorm';
import type { MysqlConnectionOptions } from '@n8n/typeorm/driver/mysql/MysqlConnectionOptions';
import type { PostgresConnectionOptions } from '@n8n/typeorm/driver/postgres/PostgresConnectionOptions';
import type { SqliteConnectionOptions } from '@n8n/typeorm/driver/sqlite/SqliteConnectionOptions';
import type { SqlitePooledConnectionOptions } from '@n8n/typeorm/driver/sqlite-pooled/SqlitePooledConnectionOptions';
import { UserError } from 'n8n-workflow';
import type { TlsOptions } from 'node:tls';
import path from 'path';

import { entities } from '../entities';
import { mysqlMigrations } from '../migrations/mysqldb';
import { postgresMigrations } from '../migrations/postgresdb';
import { sqliteMigrations } from '../migrations/sqlite';
import { subscribers } from '../subscribers';

@Service()
export class DbConnectionOptions {
	constructor(
		private readonly config: DatabaseConfig,
		private readonly instanceSettingsConfig: InstanceSettingsConfig,
		private readonly moduleRegistry: ModuleRegistry,
	) {}

	getOverrides(dbType: 'postgresdb' | 'mysqldb') {
		const dbConfig = this.config[dbType];
		return {
			database: dbConfig.database,
			host: dbConfig.host,
			port: dbConfig.port,
			username: dbConfig.user,
			password: dbConfig.password,
		};
	}

	getOptions(): DataSourceOptions {
		const { type: dbType } = this.config;
		switch (dbType) {
			case 'sqlite':
				return this.getSqliteConnectionOptions();
			case 'postgresdb':
				return this.getPostgresConnectionOptions();
			case 'mariadb':
			case 'mysqldb':
				return this.getMysqlConnectionOptions(dbType);
			default:
				throw new UserError('Database type currently not supported', { extra: { dbType } });
		}
	}

	private getCommonOptions() {
		const { tablePrefix: entityPrefix, logging: loggingConfig } = this.config;

		let loggingOption: LoggerOptions = loggingConfig.enabled;
		if (loggingOption) {
			const optionsString = loggingConfig.options.replace(/\s+/g, '');
			if (optionsString === 'all') {
				loggingOption = optionsString;
			} else {
				loggingOption = optionsString.split(',') as LoggerOptions;
			}
		}

		return {
			entityPrefix,
			entities: [...Object.values(entities), ...this.moduleRegistry.entities],
			subscribers: Object.values(subscribers),
			migrationsTableName: `${entityPrefix}migrations`,
			migrationsRun: false,
			synchronize: false,
			maxQueryExecutionTime: loggingConfig.maxQueryExecutionTime,
			logging: loggingOption,
		};
	}

	private getSqliteConnectionOptions(): SqliteConnectionOptions | SqlitePooledConnectionOptions {
		const { sqlite: sqliteConfig } = this.config;
		const { n8nFolder } = this.instanceSettingsConfig;

		const commonOptions = {
			...this.getCommonOptions(),
			database: path.resolve(n8nFolder, sqliteConfig.database),
			migrations: sqliteMigrations,
		};

		if (sqliteConfig.poolSize > 0) {
			return {
				type: 'sqlite-pooled',
				poolSize: sqliteConfig.poolSize,
				enableWAL: true,
				acquireTimeout: 60_000,
				destroyTimeout: 5_000,
				...commonOptions,
			};
		} else {
			return {
				type: 'sqlite',
				enableWAL: sqliteConfig.enableWAL,
				...commonOptions,
			};
		}
	}

	private getPostgresConnectionOptions(): PostgresConnectionOptions {
		const { postgresdb: postgresConfig } = this.config;
		const {
			ssl: { ca: sslCa, cert: sslCert, key: sslKey, rejectUnauthorized: sslRejectUnauthorized },
		} = postgresConfig;

		let ssl: TlsOptions | boolean = postgresConfig.ssl.enabled;
		if (sslCa !== '' || sslCert !== '' || sslKey !== '' || !sslRejectUnauthorized) {
			ssl = {
				ca: sslCa || undefined,
				cert: sslCert || undefined,
				key: sslKey || undefined,
				rejectUnauthorized: sslRejectUnauthorized,
			};
		}

		return {
			type: 'postgres',
			...this.getCommonOptions(),
			...this.getOverrides('postgresdb'),
			schema: postgresConfig.schema,
			poolSize: postgresConfig.poolSize,
			migrations: postgresMigrations,
			connectTimeoutMS: postgresConfig.connectionTimeoutMs,
			ssl,
			extra: {
				idleTimeoutMillis: postgresConfig.idleTimeoutMs,
			},
		};
	}

	private getMysqlConnectionOptions(dbType: 'mariadb' | 'mysqldb'): MysqlConnectionOptions {
		const { mysqldb: mysqlConfig } = this.config;
		return {
			type: dbType === 'mysqldb' ? 'mysql' : 'mariadb',
			...this.getCommonOptions(),
			...this.getOverrides('mysqldb'),
			poolSize: mysqlConfig.poolSize,
			migrations: mysqlMigrations,
			timezone: 'Z', // set UTC as default
		};
	}
}
