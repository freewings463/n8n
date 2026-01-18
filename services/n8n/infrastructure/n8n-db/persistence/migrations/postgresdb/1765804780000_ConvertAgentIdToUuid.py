"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1765804780000-ConvertAgentIdToUuid.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:ConvertAgentIdToUuid1765804780000。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1765804780000-ConvertAgentIdToUuid.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1765804780000_ConvertAgentIdToUuid.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const table = {
	sessions: 'chat_hub_sessions',
	messages: 'chat_hub_messages',
} as const;

export class ConvertAgentIdToUuid1765804780000 implements ReversibleMigration {
	async up({ runQuery, escape }: MigrationContext) {
		// Convert agentId from varchar(36) to uuid to match agents.id type
		await runQuery(
			`ALTER TABLE ${escape.tableName(table.sessions)} ALTER COLUMN "agentId" TYPE uuid USING "agentId"::uuid`,
		);
		await runQuery(
			`ALTER TABLE ${escape.tableName(table.messages)} ALTER COLUMN "agentId" TYPE uuid USING "agentId"::uuid`,
		);
	}

	async down({ runQuery, escape }: MigrationContext) {
		// Revert agentId from uuid back to varchar(36)
		await runQuery(
			`ALTER TABLE ${escape.tableName(table.sessions)} ALTER COLUMN "agentId" TYPE varchar(36)`,
		);
		await runQuery(
			`ALTER TABLE ${escape.tableName(table.messages)} ALTER COLUMN "agentId" TYPE varchar(36)`,
		);
	}
}
