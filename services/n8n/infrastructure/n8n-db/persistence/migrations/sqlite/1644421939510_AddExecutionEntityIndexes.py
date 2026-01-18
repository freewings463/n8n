"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1644421939510-AddExecutionEntityIndexes.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddExecutionEntityIndexes1644421939510。关键函数/方法:up、down。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1644421939510-AddExecutionEntityIndexes.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1644421939510_AddExecutionEntityIndexes.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddExecutionEntityIndexes1644421939510 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP INDEX IF EXISTS 'IDX_${tablePrefix}c4d999a5e90784e8caccf5589d'`);

		await queryRunner.query(`DROP INDEX IF EXISTS 'IDX_${tablePrefix}ca4a71b47f28ac6ea88293a8e2'`);

		await queryRunner.query(
			`CREATE INDEX IF NOT EXISTS 'IDX_${tablePrefix}06da892aaf92a48e7d3e400003' ON '${tablePrefix}execution_entity' ('workflowId', 'waitTill', 'id') `,
		);
		await queryRunner.query(
			`CREATE INDEX IF NOT EXISTS 'IDX_${tablePrefix}78d62b89dc1433192b86dce18a' ON '${tablePrefix}execution_entity' ('workflowId', 'finished', 'id') `,
		);
		await queryRunner.query(
			`CREATE INDEX IF NOT EXISTS 'IDX_${tablePrefix}1688846335d274033e15c846a4' ON '${tablePrefix}execution_entity' ('finished', 'id') `,
		);
		await queryRunner.query(
			`CREATE INDEX IF NOT EXISTS 'IDX_${tablePrefix}b94b45ce2c73ce46c54f20b5f9' ON '${tablePrefix}execution_entity' ('waitTill', 'id') `,
		);
		await queryRunner.query(
			`CREATE INDEX IF NOT EXISTS 'IDX_${tablePrefix}81fc04c8a17de15835713505e4' ON '${tablePrefix}execution_entity' ('workflowId', 'id') `,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP INDEX 'IDX_${tablePrefix}81fc04c8a17de15835713505e4'`);
		await queryRunner.query(`DROP INDEX 'IDX_${tablePrefix}b94b45ce2c73ce46c54f20b5f9'`);
		await queryRunner.query(`DROP INDEX 'IDX_${tablePrefix}1688846335d274033e15c846a4'`);
		await queryRunner.query(`DROP INDEX 'IDX_${tablePrefix}78d62b89dc1433192b86dce18a'`);
		await queryRunner.query(`DROP INDEX 'IDX_${tablePrefix}06da892aaf92a48e7d3e400003'`);
		await queryRunner.query(
			`CREATE INDEX 'IDX_${tablePrefix}ca4a71b47f28ac6ea88293a8e2' ON '${tablePrefix}execution_entity' ('waitTill') `,
		);
		await queryRunner.query(
			`CREATE INDEX 'IDX_${tablePrefix}c4d999a5e90784e8caccf5589d' ON '${tablePrefix}execution_entity' ('workflowId') `,
		);
	}
}
