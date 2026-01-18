"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1665484192212-CreateCredentialUsageTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateCredentialUsageTable1665484192212。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1665484192212-CreateCredentialUsageTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1665484192212_CreateCredentialUsageTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class CreateCredentialUsageTable1665484192212 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE ${tablePrefix}credential_usage (` +
				'"workflowId" int NOT NULL,' +
				'"nodeId" UUID NOT NULL,' +
				'"credentialId" int NULL,' +
				'"createdAt" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,' +
				'"updatedAt" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,' +
				`CONSTRAINT "PK_${tablePrefix}feb7a6545aa714ac6e7f6b14825f0efc9353dd3a" PRIMARY KEY ("workflowId", "nodeId", "credentialId"), ` +
				`CONSTRAINT "FK_${tablePrefix}518e1ece107b859ca6ce9ed2487f7e23" FOREIGN KEY ("workflowId") REFERENCES ${tablePrefix}workflow_entity ("id") ON DELETE CASCADE ON UPDATE CASCADE, ` +
				`CONSTRAINT "FK_${tablePrefix}7ce200a20ade7ae89fa7901da896993f" FOREIGN KEY ("credentialId") REFERENCES ${tablePrefix}credentials_entity ("id") ON DELETE CASCADE ON UPDATE CASCADE ` +
				');',
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP TABLE "${tablePrefix}credential_usage"`);
	}
}
