"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1652254514003-CommunityNodes.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CommunityNodes1652254514003。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1652254514003-CommunityNodes.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1652254514003_CommunityNodes.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class CommunityNodes1652254514003 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE \`${tablePrefix}installed_packages\` (` +
				'`packageName` char(214) NOT NULL,' +
				'`installedVersion` char(50) NOT NULL,' +
				'`authorName` char(70) NULL,' +
				'`authorEmail` char(70) NULL,' +
				'`createdAt` datetime NULL DEFAULT CURRENT_TIMESTAMP,' +
				'`updatedAt` datetime NULL DEFAULT CURRENT_TIMESTAMP,' +
				'PRIMARY KEY (`packageName`)' +
				') ENGINE=InnoDB;',
		);

		await queryRunner.query(
			`CREATE TABLE \`${tablePrefix}installed_nodes\` (` +
				'`name` char(200) NOT NULL,' +
				'`type` char(200) NOT NULL,' +
				"`latestVersion` int NOT NULL DEFAULT '1'," +
				'`package` char(214) NOT NULL,' +
				'PRIMARY KEY (`name`),' +
				`INDEX \`FK_${tablePrefix}73f857fc5dce682cef8a99c11dbddbc969618951\` (\`package\` ASC)` +
				") ENGINE='InnoDB';",
		);

		await queryRunner.query(
			`ALTER TABLE \`${tablePrefix}installed_nodes\` ADD CONSTRAINT \`FK_${tablePrefix}73f857fc5dce682cef8a99c11dbddbc969618951\` FOREIGN KEY (\`package\`) REFERENCES \`${tablePrefix}installed_packages\`(\`packageName\`) ON DELETE CASCADE ON UPDATE CASCADE`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}workflow_entity ADD UNIQUE INDEX \`IDX_${tablePrefix}943d8f922be094eb507cb9a7f9\` (\`name\`)`,
		);

		await queryRunner.query(`DROP TABLE "${tablePrefix}installed_nodes"`);
		await queryRunner.query(`DROP TABLE "${tablePrefix}installed_packages"`);
	}
}
