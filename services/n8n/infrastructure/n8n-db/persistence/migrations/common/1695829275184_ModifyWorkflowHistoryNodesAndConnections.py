"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1695829275184-ModifyWorkflowHistoryNodesAndConnections.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:ModifyWorkflowHistoryNodesAndConnections1695829275184。关键函数/方法:up、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1695829275184-ModifyWorkflowHistoryNodesAndConnections.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1695829275184_ModifyWorkflowHistoryNodesAndConnections.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const tableName = 'workflow_history';

export class ModifyWorkflowHistoryNodesAndConnections1695829275184 implements ReversibleMigration {
	async up({ schemaBuilder: { addColumns, dropColumns, column } }: MigrationContext) {
		await dropColumns(tableName, ['nodes', 'connections']);
		await addColumns(tableName, [column('nodes').json.notNull, column('connections').json.notNull]);
	}

	async down({ schemaBuilder: { dropColumns, addColumns, column } }: MigrationContext) {
		await dropColumns(tableName, ['nodes', 'connections']);
		await addColumns(tableName, [column('nodes').text.notNull, column('connections').text.notNull]);
	}
}
