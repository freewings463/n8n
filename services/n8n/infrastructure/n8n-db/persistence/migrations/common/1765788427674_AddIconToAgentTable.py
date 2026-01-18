"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1765788427674-AddIconToAgentTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddIconToAgentTable1765788427674。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1765788427674-AddIconToAgentTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1765788427674_AddIconToAgentTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const table = 'chat_hub_agents';

export class AddIconToAgentTable1765788427674 implements ReversibleMigration {
	async up({ schemaBuilder: { addColumns, column } }: MigrationContext) {
		// Add icon column to agents table (nullable)
		await addColumns(table, [column('icon').json]);
	}

	async down({ schemaBuilder: { dropColumns } }: MigrationContext) {
		// Drop icon column
		await dropColumns(table, ['icon']);
	}
}
