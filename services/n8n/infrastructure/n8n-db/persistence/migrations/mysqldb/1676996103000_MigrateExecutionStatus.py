"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1676996103000-MigrateExecutionStatus.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:MigrateExecutionStatus1676996103000。关键函数/方法:up。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1676996103000-MigrateExecutionStatus.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1676996103000_MigrateExecutionStatus.py

import type { MigrationContext, IrreversibleMigration } from '../migration-types';

export class MigrateExecutionStatus1676996103000 implements IrreversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`UPDATE \`${tablePrefix}execution_entity\` SET status='waiting' WHERE status IS NULL AND \`waitTill\` IS NOT NULL;`,
		);
		await queryRunner.query(
			`UPDATE \`${tablePrefix}execution_entity\` SET status='failed' WHERE status IS NULL AND finished=0 AND \`stoppedAt\` IS NOT NULL;`,
		);
		await queryRunner.query(
			`UPDATE \`${tablePrefix}execution_entity\` SET status='success' WHERE status IS NULL AND finished=1 AND \`stoppedAt\` IS NOT NULL;`,
		);
		await queryRunner.query(
			`UPDATE \`${tablePrefix}execution_entity\` SET status='crashed' WHERE status IS NULL;`,
		);
	}
}
