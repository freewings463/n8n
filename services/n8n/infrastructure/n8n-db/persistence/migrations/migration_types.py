"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/migration-types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations 的类型。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/typeorm；本地:./dsl。导出:DatabaseType、MigrationContext、MigrationFn、BaseMigration、ReversibleMigration、IrreversibleMigration、Migration、InsertResult 等1项。关键函数/方法:loadSurveyFromDisk、columnName、tableName、indexName、copyTable。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/migration-types.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/migration_types.py

import type { Logger } from '@n8n/backend-common';
import type { QueryRunner, ObjectLiteral } from '@n8n/typeorm';

import type { createSchemaBuilder } from './dsl';

export type DatabaseType = 'mariadb' | 'postgresdb' | 'mysqldb' | 'sqlite';

export interface MigrationContext {
	logger: Logger;
	queryRunner: QueryRunner;
	tablePrefix: string;
	dbType: DatabaseType;
	isMysql: boolean;
	isSqlite: boolean;
	isPostgres: boolean;
	dbName: string;
	migrationName: string;
	schemaBuilder: ReturnType<typeof createSchemaBuilder>;
	loadSurveyFromDisk(): string | null;
	parseJson<T>(data: string | T): T;
	escape: {
		columnName(name: string): string;
		tableName(name: string): string;
		indexName(name: string): string;
	};
	runQuery<T>(sql: string, namedParameters?: ObjectLiteral): Promise<T>;
	runInBatches<T>(
		query: string,
		operation: (results: T[]) => Promise<void>,
		limit?: number,
	): Promise<void>;
	copyTable(fromTable: string, toTable: string): Promise<void>;
	copyTable(
		fromTable: string,
		toTable: string,
		fromFields?: string[],
		toFields?: string[],
		batchSize?: number,
	): Promise<void>;
}

export type MigrationFn = (ctx: MigrationContext) => Promise<void>;

export interface BaseMigration {
	up: MigrationFn;
	// eslint-disable-next-line @typescript-eslint/no-redundant-type-constituents
	down?: MigrationFn | never;
	transaction?: false;
}

export interface ReversibleMigration extends BaseMigration {
	down: MigrationFn;
}

export interface IrreversibleMigration extends BaseMigration {
	down?: never;
}

// eslint-disable-next-line @typescript-eslint/no-restricted-types
export interface Migration extends Function {
	prototype: ReversibleMigration | IrreversibleMigration;
}

export type InsertResult = Array<{ insertId: number }>;

export { QueryFailedError } from '@n8n/typeorm/error/QueryFailedError';
