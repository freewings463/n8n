"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1592447867632-WebhookModel.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:WebhookModel1592447867632。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1592447867632-WebhookModel.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1592447867632_WebhookModel.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class WebhookModel1592447867632 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE IF NOT EXISTS ${tablePrefix}webhook_entity (workflowId int NOT NULL, webhookPath varchar(255) NOT NULL, method varchar(255) NOT NULL, node varchar(255) NOT NULL, PRIMARY KEY (webhookPath, method)) ENGINE=InnoDB`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP TABLE ${tablePrefix}webhook_entity`);
	}
}
