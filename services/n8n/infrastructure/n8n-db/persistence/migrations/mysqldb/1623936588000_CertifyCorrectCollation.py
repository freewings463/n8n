"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1623936588000-CertifyCorrectCollation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CertifyCorrectCollation1623936588000。关键函数/方法:up、checkCollationExistence。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1623936588000-CertifyCorrectCollation.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1623936588000_CertifyCorrectCollation.py

import type { MigrationContext, IrreversibleMigration } from '../migration-types';

export class CertifyCorrectCollation1623936588000 implements IrreversibleMigration {
	async up({ queryRunner, tablePrefix, dbType, dbName }: MigrationContext) {
		if (dbType === 'mariadb') {
			// This applies to MySQL only.
			return;
		}

		const checkCollationExistence = (await queryRunner.query(
			"show collation where collation like 'utf8mb4_0900_ai_ci';",
		)) as unknown[];
		let collation = 'utf8mb4_general_ci';
		if (checkCollationExistence.length > 0) {
			collation = 'utf8mb4_0900_ai_ci';
		}

		await queryRunner.query(
			`ALTER DATABASE \`${dbName}\` CHARACTER SET utf8mb4 COLLATE ${collation};`,
		);

		for (const tableName of [
			'credentials_entity',
			'execution_entity',
			'tag_entity',
			'webhook_entity',
			'workflow_entity',
			'workflows_tags',
		]) {
			await queryRunner.query(
				`ALTER TABLE ${tablePrefix}${tableName} CONVERT TO CHARACTER SET utf8mb4 COLLATE ${collation};`,
			);
		}
	}

	// There is no down migration in this case as we already expect default collation to be utf8mb4
	// The up migration exists simply to enforce that n8n will work with older mysql versions
}
