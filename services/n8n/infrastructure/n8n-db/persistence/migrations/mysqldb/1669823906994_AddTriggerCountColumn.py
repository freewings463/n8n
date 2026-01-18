"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1669823906994-AddTriggerCountColumn.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddTriggerCountColumn1669823906994。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1669823906994-AddTriggerCountColumn.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1669823906994_AddTriggerCountColumn.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddTriggerCountColumn1669823906994 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`ALTER TABLE ${tablePrefix}workflow_entity ADD COLUMN triggerCount integer NOT NULL DEFAULT 0`,
		);
		// Table will be populated by n8n startup - see ActiveWorkflowManager.ts
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`ALTER TABLE ${tablePrefix}workflow_entity DROP COLUMN triggerCount`);
	}
}
