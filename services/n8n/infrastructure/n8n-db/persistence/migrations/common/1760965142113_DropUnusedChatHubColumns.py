"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1760965142113-DropUnusedChatHubColumns.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:DropUnusedChatHubColumns1760965142113。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1760965142113-DropUnusedChatHubColumns.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1760965142113_DropUnusedChatHubColumns.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const table = {
	messages: 'chat_hub_messages',
} as const;

export class DropUnusedChatHubColumns1760965142113 implements ReversibleMigration {
	async up({ schemaBuilder: { dropColumns, addColumns, column } }: MigrationContext) {
		await dropColumns(table.messages, ['turnId', 'runIndex', 'state']);
		await addColumns(table.messages, [
			column('status')
				.varchar(16)
				.default("'success'")
				.notNull.comment(
					'ChatHubMessageStatus enum, eg. "success", "error", "running", "cancelled"',
				),
		]);
	}

	async down({
		schemaBuilder: { dropColumns, addColumns, column, addForeignKey },
	}: MigrationContext) {
		await dropColumns(table.messages, ['status']);
		await addColumns(table.messages, [
			column('turnId').uuid,
			column('runIndex')
				.int.notNull.default(0)
				.comment('The nth attempt this message has been generated/retried this turn'),
			column('state')
				.varchar(16)
				.default("'active'")
				.notNull.comment('ChatHubMessageState enum: "active", "superseded", "hidden", "deleted"'),
		]);
		await addForeignKey(table.messages, 'turnId', [table.messages, 'id'], undefined, 'CASCADE');
	}
}
