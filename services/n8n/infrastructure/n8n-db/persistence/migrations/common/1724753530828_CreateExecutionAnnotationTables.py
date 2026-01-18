"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1724753530828-CreateExecutionAnnotationTables.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateAnnotationTables1724753530828。关键函数/方法:up、column、down。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1724753530828-CreateExecutionAnnotationTables.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1724753530828_CreateExecutionAnnotationTables.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const annotationsTableName = 'execution_annotations';
const annotationTagsTableName = 'annotation_tag_entity';
const annotationTagMappingsTableName = 'execution_annotation_tags';

export class CreateAnnotationTables1724753530828 implements ReversibleMigration {
	async up({ schemaBuilder: { createTable, column } }: MigrationContext) {
		await createTable(annotationsTableName)
			.withColumns(
				column('id').int.notNull.primary.autoGenerate,
				column('executionId').int.notNull,
				column('vote').varchar(6),
				column('note').text,
			)
			.withIndexOn('executionId', true)
			.withForeignKey('executionId', {
				tableName: 'execution_entity',
				columnName: 'id',
				onDelete: 'CASCADE',
			}).withTimestamps;

		await createTable(annotationTagsTableName)
			.withColumns(column('id').varchar(16).primary.notNull, column('name').varchar(24).notNull)
			.withIndexOn('name', true).withTimestamps;

		await createTable(annotationTagMappingsTableName)
			.withColumns(
				column('annotationId').int.notNull.primary,
				column('tagId').varchar(24).notNull.primary,
			)
			.withForeignKey('annotationId', {
				tableName: annotationsTableName,
				columnName: 'id',
				onDelete: 'CASCADE',
			})
			.withIndexOn('tagId')
			.withIndexOn('annotationId')
			.withForeignKey('tagId', {
				tableName: annotationTagsTableName,
				columnName: 'id',
				onDelete: 'CASCADE',
			});
	}

	async down({ schemaBuilder: { dropTable } }: MigrationContext) {
		await dropTable(annotationTagMappingsTableName);
		await dropTable(annotationTagsTableName);
		await dropTable(annotationsTableName);
	}
}
