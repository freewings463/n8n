"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1721377157740-FixExecutionMetadataSequence.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:FixExecutionMetadataSequence1721377157740。关键函数/方法:up。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1721377157740-FixExecutionMetadataSequence.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1721377157740_FixExecutionMetadataSequence.py

import type { IrreversibleMigration, MigrationContext } from '../migration-types';

export class FixExecutionMetadataSequence1721377157740 implements IrreversibleMigration {
	async up({ queryRunner, escape }: MigrationContext) {
		const tableName = escape.tableName('execution_metadata');
		const sequenceName = escape.tableName('execution_metadata_temp_id_seq');

		await queryRunner.query(
			`SELECT setval('${sequenceName}', (SELECT MAX(id) FROM ${tableName}));`,
		);
	}
}
