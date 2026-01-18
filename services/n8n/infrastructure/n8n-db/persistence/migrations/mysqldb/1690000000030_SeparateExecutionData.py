"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1690000000030-SeparateExecutionData.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:SeparateExecutionData1690000000030。关键函数/方法:up、down。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1690000000030-SeparateExecutionData.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1690000000030_SeparateExecutionData.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class SeparateExecutionData1690000000030 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE ${tablePrefix}execution_data (
				executionId int(11) NOT NULL primary key,
				workflowData json NOT NULL,
				data MEDIUMTEXT NOT NULL,
				CONSTRAINT \`${tablePrefix}execution_data_FK\` FOREIGN KEY (\`executionId\`) REFERENCES \`${tablePrefix}execution_entity\` (\`id\`) ON DELETE CASCADE
			)
			ENGINE=InnoDB`,
		);

		await queryRunner.query(
			`INSERT INTO ${tablePrefix}execution_data (
				executionId,
				workflowData,
				data)
				SELECT id, workflowData, data FROM ${tablePrefix}execution_entity
			`,
		);

		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}execution_entity DROP COLUMN workflowData, DROP COLUMN data`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}execution_entity
			ADD workflowData json NULL,
			ADD data MEDIUMTEXT NULL`,
		);

		await queryRunner.query(
			`UPDATE ${tablePrefix}execution_entity SET workflowData = ${tablePrefix}execution_data.workflowData, data = ${tablePrefix}execution_data.data
			FROM ${tablePrefix}execution_data WHERE ${tablePrefix}execution_data.executionId = ${tablePrefix}execution_entity.id`,
		);

		await queryRunner.query(`DROP TABLE ${tablePrefix}execution_data`);
	}
}
