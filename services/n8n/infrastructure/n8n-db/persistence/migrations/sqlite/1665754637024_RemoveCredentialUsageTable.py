"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1665754637024-RemoveCredentialUsageTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:RemoveCredentialUsageTable1665754637024。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1665754637024-RemoveCredentialUsageTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1665754637024_RemoveCredentialUsageTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class RemoveCredentialUsageTable1665754637024 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP TABLE "${tablePrefix}credential_usage"`);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE "${tablePrefix}credential_usage" (` +
				'"workflowId"	integer NOT NULL,' +
				'"nodeId"	varchar NOT NULL,' +
				'"credentialId"	integer NOT NULL,' +
				"\"createdAt\"	datetime(3) NOT NULL DEFAULT 'STRFTIME(''%Y-%m-%d %H:%M:%f'', ''NOW'')'," +
				"\"updatedAt\"	datetime(3) NOT NULL DEFAULT 'STRFTIME(''%Y-%m-%d %H:%M:%f'', ''NOW'')'," +
				'PRIMARY KEY("workflowId", "nodeId", "credentialId"), ' +
				`CONSTRAINT "FK_${tablePrefix}518e1ece107b859ca6ce9ed2487f7e23" FOREIGN KEY ("workflowId") REFERENCES "${tablePrefix}workflow_entity" ("id") ON DELETE CASCADE ON UPDATE NO ACTION, ` +
				`CONSTRAINT "FK_${tablePrefix}7ce200a20ade7ae89fa7901da896993f" FOREIGN KEY ("credentialId") REFERENCES "${tablePrefix}credentials_entity" ("id") ON DELETE CASCADE ON UPDATE NO ACTION ` +
				');',
		);
	}
}
