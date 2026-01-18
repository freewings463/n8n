"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src 的入口。导入/依赖:外部:无；内部:无；本地:无。再导出:./constants、./entities、./entities/types-db、./repositories 等2项。导出:generateNanoId、isStringArray、isValidEmail、separate、sql、idStringifier、lowerCaser、objectRetriever 等17项。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/db entrypoint -> infrastructure/persistence/__init__.py
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/index.ts -> services/n8n/infrastructure/n8n-db/persistence/__init__.py

export {
	WithStringId,
	WithTimestamps,
	WithTimestampsAndStringId,
	jsonColumnType,
	datetimeColumnType,
	dbType,
	JsonColumn,
	DateTimeColumn,
} from './entities/abstract-entity';

export { generateNanoId } from './utils/generators';
export { isStringArray } from './utils/is-string-array';
export { isValidEmail } from './utils/is-valid-email';
export { separate } from './utils/separate';
export { sql } from './utils/sql';
export { idStringifier, lowerCaser, objectRetriever, sqlite } from './utils/transformers';
export { withTransaction } from './utils/transaction';

export * from './constants';
export * from './entities';
export * from './entities/types-db';
export { NoXss } from './utils/validators/no-xss.validator';
export { NoUrl } from './utils/validators/no-url.validator';

export * from './repositories';
export * from './subscribers';

export { Column as DslColumn } from './migrations/dsl/column';
export { CreateTable } from './migrations/dsl/table';
export { sqliteMigrations } from './migrations/sqlite';
export { mysqlMigrations } from './migrations/mysqldb';
export { postgresMigrations } from './migrations/postgresdb';

export { wrapMigration } from './migrations/migration-helpers';
export * from './migrations/migration-types';
export { DbConnection } from './connection/db-connection';
export { DbConnectionOptions } from './connection/db-connection-options';

export { AuthRolesService } from './services/auth.roles.service';

export { In, Like, Not, DataSource } from '@n8n/typeorm';
export type { FindOptionsWhere } from '@n8n/typeorm';
export type { EntityManager } from '@n8n/typeorm';
