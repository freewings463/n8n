"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1677501636753-CreateVariables.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateVariables1677501636753。关键函数/方法:up、UNIQUE、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1677501636753-CreateVariables.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1677501636753_CreateVariables.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class CreateVariables1677501636753 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`
			CREATE TABLE ${tablePrefix}variables (
				id int(11) auto_increment NOT NULL PRIMARY KEY,
				\`key\` VARCHAR(50) NOT NULL,
				\`type\` VARCHAR(50) DEFAULT 'string' NOT NULL,
				value VARCHAR(255) NULL,
				UNIQUE (\`key\`)
			)
			ENGINE=InnoDB;
		`);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP TABLE ${tablePrefix}variables;`);
	}
}
