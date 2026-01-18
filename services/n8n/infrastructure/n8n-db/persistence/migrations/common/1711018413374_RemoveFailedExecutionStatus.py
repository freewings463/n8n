"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1711018413374-RemoveFailedExecutionStatus.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:RemoveFailedExecutionStatus1711018413374。关键函数/方法:up。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1711018413374-RemoveFailedExecutionStatus.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1711018413374_RemoveFailedExecutionStatus.py

import type { IrreversibleMigration, MigrationContext } from '../migration-types';

export class RemoveFailedExecutionStatus1711018413374 implements IrreversibleMigration {
	async up({ escape, runQuery }: MigrationContext) {
		const executionEntity = escape.tableName('execution_entity');

		await runQuery(`UPDATE ${executionEntity} SET status = 'error' WHERE status = 'failed';`);
	}
}
