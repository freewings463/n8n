"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1652254514002-CommunityNodes.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CommunityNodes1652254514002。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1652254514002-CommunityNodes.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1652254514002_CommunityNodes.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class CommunityNodes1652254514002 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE ${tablePrefix}installed_packages (` +
				'"packageName" VARCHAR(214) NOT NULL,' +
				'"installedVersion" VARCHAR(50) NOT NULL,' +
				'"authorName" VARCHAR(70) NULL,' +
				'"authorEmail" VARCHAR(70) NULL,' +
				'"createdAt" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,' +
				'"updatedAt" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,' +
				`CONSTRAINT "PK_${tablePrefix}08cc9197c39b028c1e9beca225940576fd1a5804" PRIMARY KEY ("packageName")` +
				');',
		);

		await queryRunner.query(
			`CREATE TABLE ${tablePrefix}installed_nodes (` +
				'"name" VARCHAR(200) NOT NULL, ' +
				'"type" VARCHAR(200) NOT NULL, ' +
				'"latestVersion" integer NOT NULL DEFAULT 1, ' +
				'"package" VARCHAR(241) NOT NULL, ' +
				`CONSTRAINT "PK_${tablePrefix}8ebd28194e4f792f96b5933423fc439df97d9689" PRIMARY KEY ("name"), ` +
				`CONSTRAINT "FK_${tablePrefix}73f857fc5dce682cef8a99c11dbddbc969618951" FOREIGN KEY ("package") REFERENCES ${tablePrefix}installed_packages ("packageName") ON DELETE CASCADE ON UPDATE CASCADE ` +
				');',
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP TABLE "${tablePrefix}installed_nodes"`);
		await queryRunner.query(`DROP TABLE "${tablePrefix}installed_packages"`);
	}
}
