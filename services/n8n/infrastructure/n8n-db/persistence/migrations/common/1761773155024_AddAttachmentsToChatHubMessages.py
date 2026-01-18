"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1761773155024-AddAttachmentsToChatHubMessages.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddAttachmentsToChatHubMessages1761773155024。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1761773155024-AddAttachmentsToChatHubMessages.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1761773155024_AddAttachmentsToChatHubMessages.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const table = {
	messages: 'chat_hub_messages',
} as const;

export class AddAttachmentsToChatHubMessages1761773155024 implements ReversibleMigration {
	async up({ schemaBuilder: { addColumns, column } }: MigrationContext) {
		await addColumns(table.messages, [
			column('attachments').json.comment(
				'File attachments for the message (if any), stored as JSON. Files are stored as base64-encoded data URLs.',
			),
		]);
	}

	async down({ schemaBuilder: { dropColumns } }: MigrationContext) {
		await dropColumns(table.messages, ['attachments']);
	}
}
