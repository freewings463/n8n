"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1665484192213-CreateCredentialUsageTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateCredentialUsageTable1665484192213。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1665484192213-CreateCredentialUsageTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1665484192213_CreateCredentialUsageTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class CreateCredentialUsageTable1665484192213 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE \`${tablePrefix}credential_usage\` (` +
				'`workflowId` int NOT NULL,' +
				'`nodeId` char(200) NOT NULL,' +
				"`credentialId` int NOT NULL DEFAULT '1'," +
				'`createdAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,' +
				'`updatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,' +
				'PRIMARY KEY (`workflowId`, `nodeId`, `credentialId`)' +
				") ENGINE='InnoDB';",
		);

		await queryRunner.query(
			`ALTER TABLE \`${tablePrefix}credential_usage\` ADD CONSTRAINT \`FK_${tablePrefix}518e1ece107b859ca6ce9ed2487f7e23\` FOREIGN KEY (\`workflowId\`) REFERENCES \`${tablePrefix}workflow_entity\`(\`id\`) ON DELETE CASCADE ON UPDATE CASCADE`,
		);

		await queryRunner.query(
			`ALTER TABLE \`${tablePrefix}credential_usage\` ADD CONSTRAINT \`FK_${tablePrefix}7ce200a20ade7ae89fa7901da896993f\` FOREIGN KEY (\`credentialId\`) REFERENCES \`${tablePrefix}credentials_entity\`(\`id\`) ON DELETE CASCADE ON UPDATE CASCADE`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP TABLE "${tablePrefix}credential_usage"`);
	}
}
