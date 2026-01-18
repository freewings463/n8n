"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1760019379982-CreateChatHubTables.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateChatHubTables1760019379982。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1760019379982-CreateChatHubTables.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1760019379982_CreateChatHubTables.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const table = {
	sessions: 'chat_hub_sessions',
	messages: 'chat_hub_messages',
	user: 'user',
	credentials: 'credentials_entity',
	workflows: 'workflow_entity',
	executions: 'execution_entity',
} as const;

export class CreateChatHubTables1760019379982 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column } }: MigrationContext) {
		await createTable(table.sessions)
			.withColumns(
				column('id').uuid.primary,
				column('title').varchar(256).notNull,
				column('ownerId').uuid.notNull,
				column('lastMessageAt').timestampTimezone(),

				column('credentialId').varchar(36),
				column('provider')
					.varchar(16)
					.comment('ChatHubProvider enum: "openai", "anthropic", "google", "n8n"'),
				column('model')
					.varchar(64)
					.comment('Model name used at the respective Model node, ie. "gpt-4"'),
				column('workflowId').varchar(36),
			)
			.withForeignKey('ownerId', {
				tableName: table.user,
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withForeignKey('credentialId', {
				tableName: table.credentials,
				columnName: 'id',
				onDelete: 'SET NULL',
			})
			.withForeignKey('workflowId', {
				tableName: table.workflows,
				columnName: 'id',
				onDelete: 'SET NULL',
			}).withTimestamps;

		await createTable(table.messages)
			.withColumns(
				column('id').uuid.primary.notNull,
				column('sessionId').uuid.notNull,
				column('previousMessageId').uuid,
				column('revisionOfMessageId').uuid,
				column('turnId').uuid,
				column('retryOfMessageId').uuid,
				column('type')
					.varchar(16)
					.notNull.comment('ChatHubMessageType enum: "human", "ai", "system", "tool", "generic"'),
				column('name').varchar(128).notNull,
				column('state')
					.varchar(16)
					.default("'active'")
					.notNull.comment('ChatHubMessageState enum: "active", "superseded", "hidden", "deleted"'),
				column('content').text.notNull,
				column('provider')
					.varchar(16)
					.comment('ChatHubProvider enum: "openai", "anthropic", "google", "n8n"'),
				column('model')
					.varchar(64)
					.comment('Model name used at the respective Model node, ie. "gpt-4"'),
				column('workflowId').varchar(36),
				column('runIndex')
					.int.notNull.default(0)
					.comment('The nth attempt this message has been generated/retried this turn'),
				column('executionId').int,
			)
			.withForeignKey('sessionId', {
				tableName: table.sessions,
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withForeignKey('previousMessageId', {
				tableName: table.messages,
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withForeignKey('workflowId', {
				tableName: table.workflows,
				columnName: 'id',
				onDelete: 'SET NULL',
			})
			.withForeignKey('turnId', {
				tableName: table.messages,
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withForeignKey('retryOfMessageId', {
				tableName: table.messages,
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withForeignKey('revisionOfMessageId', {
				tableName: table.messages,
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withForeignKey('executionId', {
				tableName: table.executions,
				columnName: 'id',
				onDelete: 'SET NULL',
			}).withTimestamps;
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(table.messages);
		await dropTable(table.sessions);
	}
}
