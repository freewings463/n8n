"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1731582748663-MigrateTestDefinitionKeyToString.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:MigrateTestDefinitionKeyToString1731582748663。关键函数/方法:up。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1731582748663-MigrateTestDefinitionKeyToString.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1731582748663_MigrateTestDefinitionKeyToString.py

import type { MigrationContext, IrreversibleMigration } from '../migration-types';

export class MigrateTestDefinitionKeyToString1731582748663 implements IrreversibleMigration {
	async up(context: MigrationContext) {
		const { queryRunner, tablePrefix } = context;

		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}test_definition RENAME COLUMN id to tmp_id;`,
		);
		await queryRunner.query(`ALTER TABLE ${tablePrefix}test_definition ADD COLUMN id varchar(36);`);
		await queryRunner.query(`UPDATE ${tablePrefix}test_definition SET id = tmp_id::text;`);
		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}test_definition ALTER COLUMN id SET NOT NULL;`,
		);
		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}test_definition ALTER COLUMN tmp_id DROP DEFAULT;`,
		);
		await queryRunner.query(`DROP SEQUENCE IF EXISTS ${tablePrefix}test_definition_id_seq;`);
		await queryRunner.query(
			`CREATE UNIQUE INDEX "pk_${tablePrefix}test_definition_id" ON ${tablePrefix}test_definition ("id");`,
		);

		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}test_definition DROP CONSTRAINT IF EXISTS "PK_${tablePrefix}245a0013672c8cdc7727afa9b99";`,
		);

		await queryRunner.query(`ALTER TABLE ${tablePrefix}test_definition DROP COLUMN tmp_id;`);
		await queryRunner.query(`ALTER TABLE ${tablePrefix}test_definition ADD PRIMARY KEY (id);`);
	}
}
