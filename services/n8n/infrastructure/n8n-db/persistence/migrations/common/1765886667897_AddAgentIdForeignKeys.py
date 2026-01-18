"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1765886667897-AddAgentIdForeignKeys.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddAgentIdForeignKeys1765886667897。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1765886667897-AddAgentIdForeignKeys.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1765886667897_AddAgentIdForeignKeys.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const table = {
	agents: 'chat_hub_agents',
	sessions: 'chat_hub_sessions',
	messages: 'chat_hub_messages',
} as const;

export class AddAgentIdForeignKeys1765886667897 implements ReversibleMigration {
	async up({ schemaBuilder: { addForeignKey }, runQuery, escape }: MigrationContext) {
		const escapedAgentIdColumn = escape.columnName('agentId');

		// Clean up orphaned agentId references before adding foreign key constraint
		await runQuery(
			`UPDATE ${escape.tableName(table.sessions)} SET ${escapedAgentIdColumn} = NULL WHERE ${escapedAgentIdColumn} IS NOT NULL AND ${escapedAgentIdColumn} NOT IN (SELECT id FROM ${escape.tableName(table.agents)})`,
		);
		await runQuery(
			`UPDATE ${escape.tableName(table.messages)} SET ${escapedAgentIdColumn} = NULL WHERE ${escapedAgentIdColumn} IS NOT NULL AND ${escapedAgentIdColumn} NOT IN (SELECT id FROM ${escape.tableName(table.agents)})`,
		);

		// Add foreign key constraint for agentId in sessions table
		await addForeignKey(
			table.sessions,
			'agentId',
			[table.agents, 'id'],
			'FK_chat_hub_sessions_agentId',
			'SET NULL',
		);
		await addForeignKey(
			table.messages,
			'agentId',
			[table.agents, 'id'],
			'FK_chat_hub_messages_agentId',
			'SET NULL',
		);
	}

	async down({ schemaBuilder: { dropForeignKey } }: MigrationContext) {
		await dropForeignKey(
			table.messages,
			'agentId',
			[table.agents, 'id'],
			'FK_chat_hub_messages_agentId',
		);
		await dropForeignKey(
			table.sessions,
			'agentId',
			[table.agents, 'id'],
			'FK_chat_hub_sessions_agentId',
		);
	}
}
