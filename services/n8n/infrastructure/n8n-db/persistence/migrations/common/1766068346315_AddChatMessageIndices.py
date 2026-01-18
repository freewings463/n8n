"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1766068346315-AddChatMessageIndices.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddChatMessageIndices1766068346315。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1766068346315-AddChatMessageIndices.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1766068346315_AddChatMessageIndices.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddChatMessageIndices1766068346315 implements ReversibleMigration {
	async up({ schemaBuilder: { addNotNull }, runQuery, escape }: MigrationContext) {
		const sessionsTable = escape.tableName('chat_hub_sessions');
		const idColumn = escape.columnName('id');
		const createdAtColumn = escape.columnName('createdAt');
		const ownerIdColumn = escape.columnName('ownerId');
		const lastMessageAtColumn = escape.columnName('lastMessageAt');

		const messagesTable = escape.tableName('chat_hub_messages');
		const sessionIdColumn = escape.columnName('sessionId');

		// Backfill lastMessageAt for existing rows to allow adding a NOT NULL constraint
		await runQuery(
			`UPDATE ${sessionsTable}
			SET ${lastMessageAtColumn} = ${createdAtColumn}
			WHERE ${lastMessageAtColumn} IS NULL`,
		);

		await addNotNull('chat_hub_sessions', 'lastMessageAt');

		// Index intended for faster sessionRepository.getManyByUserId queries
		await runQuery(
			`CREATE INDEX IF NOT EXISTS ${escape.indexName('chat_hub_sessions_owner_lastmsg_id')}
			ON ${sessionsTable}(${ownerIdColumn}, ${lastMessageAtColumn} DESC, ${idColumn})`,
		);

		// Index intended for faster sessionRepository.getOneByIdAndUserId queries and joins
		await runQuery(
			`CREATE INDEX IF NOT EXISTS ${escape.indexName('chat_hub_messages_sessionId')}
			ON ${messagesTable}(${sessionIdColumn})`,
		);
	}

	async down({ schemaBuilder: { dropNotNull }, runQuery, escape }: MigrationContext) {
		await runQuery(
			`DROP INDEX IF EXISTS ${escape.indexName('chat_hub_sessions_owner_lastmsg_id')}`,
		);
		await runQuery(`DROP INDEX IF EXISTS ${escape.indexName('chat_hub_messages_sessionId')}`);

		await dropNotNull('chat_hub_sessions', 'lastMessageAt');
	}
}
