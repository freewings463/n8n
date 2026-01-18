"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1652905585850-AddAPIKeyColumn.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddAPIKeyColumn1652905585850。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1652905585850-AddAPIKeyColumn.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1652905585850_AddAPIKeyColumn.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddAPIKeyColumn1652905585850 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`ALTER TABLE "${tablePrefix}user" ADD COLUMN "apiKey" VARCHAR(255)`);
		await queryRunner.query(
			`CREATE UNIQUE INDEX "UQ_${tablePrefix}ie0zomxves9w3p774drfrkxtj5" ON "${tablePrefix}user" ("apiKey")`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP INDEX "UQ_${tablePrefix}ie0zomxves9w3p774drfrkxtj5"`);
		await queryRunner.query(`ALTER TABLE "${tablePrefix}user" DROP COLUMN "apiKey"`);
	}
}
