"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1731582748663-MigrateTestDefinitionKeyToString.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:MigrateTestDefinitionKeyToString1731582748663。关键函数/方法:up。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1731582748663-MigrateTestDefinitionKeyToString.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1731582748663_MigrateTestDefinitionKeyToString.py

import type { MigrationContext, IrreversibleMigration } from '../migration-types';

export class MigrateTestDefinitionKeyToString1731582748663 implements IrreversibleMigration {
	async up(context: MigrationContext) {
		const { queryRunner, tablePrefix } = context;

		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}test_definition CHANGE id tmp_id int NOT NULL AUTO_INCREMENT;`,
		);
		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}test_definition ADD COLUMN id varchar(36) NOT NULL;`,
		);
		await queryRunner.query(`UPDATE ${tablePrefix}test_definition SET id = CONVERT(tmp_id, CHAR);`);
		await queryRunner.query(
			`CREATE INDEX \`TMP_idx_${tablePrefix}test_definition_id\` ON ${tablePrefix}test_definition (\`id\`);`,
		);

		// Note: this part was missing in initial release and was added after. Without it the migration run successfully,
		// but left the table in inconsistent state, because it didn't finish changing the primary key and deleting the old one.
		// This prevented the next migration from running on MySQL 8.4.4
		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}test_definition MODIFY COLUMN tmp_id INT NOT NULL;`,
		);
		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}test_definition DROP PRIMARY KEY, ADD PRIMARY KEY (\`id\`);`,
		);
		await queryRunner.query(
			`DROP INDEX \`TMP_idx_${tablePrefix}test_definition_id\` ON ${tablePrefix}test_definition;`,
		);
		await queryRunner.query(`ALTER TABLE ${tablePrefix}test_definition DROP COLUMN tmp_id;`);
	}
}
