"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1695128658538-AddWorkflowMetadata.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddWorkflowMetadata1695128658538。关键函数/方法:up、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1695128658538-AddWorkflowMetadata.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1695128658538_AddWorkflowMetadata.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddWorkflowMetadata1695128658538 implements ReversibleMigration {
	async up({ schemaBuilder: { addColumns, column } }: MigrationContext) {
		await addColumns('workflow_entity', [column('meta').json]);
	}

	async down({ schemaBuilder: { dropColumns } }: MigrationContext) {
		await dropColumns('workflow_entity', ['meta']);
	}
}
