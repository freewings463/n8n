"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1761830340990-AddToolsColumnToChatHubTables.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddToolsColumnToChatHubTables1761830340990。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1761830340990-AddToolsColumnToChatHubTables.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1761830340990_AddToolsColumnToChatHubTables.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const table = {
	sessions: 'chat_hub_sessions',
	agents: 'chat_hub_agents',
} as const;

export class AddToolsColumnToChatHubTables1761830340990 implements ReversibleMigration {
	async up({ schemaBuilder: { addColumns, column }, queryRunner, tablePrefix }: MigrationContext) {
		await addColumns(table.sessions, [
			column('tools').json.notNull.comment('Tools available to the agent as JSON node definitions'),
		]);
		await addColumns(table.agents, [
			column('tools').json.notNull.comment('Tools available to the agent as JSON node definitions'),
		]);

		// Add a default value for existing rows
		await Promise.all(
			[
				`UPDATE \`${tablePrefix}${table.sessions}\` SET \`tools\` = '[]' WHERE JSON_TYPE(\`tools\`) = 'NULL'`,
				`UPDATE \`${tablePrefix}${table.agents}\` SET \`tools\` = '[]' WHERE JSON_TYPE(\`tools\`) = 'NULL'`,
			].map(async (query) => {
				await queryRunner.query(query);
			}),
		);
	}

	async down({ schemaBuilder: { dropColumns } }: MigrationContext) {
		await dropColumns(table.sessions, ['tools']);
		await dropColumns(table.agents, ['tools']);
	}
}
