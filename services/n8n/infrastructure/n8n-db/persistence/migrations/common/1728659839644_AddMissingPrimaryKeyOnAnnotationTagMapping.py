"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1728659839644-AddMissingPrimaryKeyOnAnnotationTagMapping.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:node:assert；内部:无；本地:../migration-types。导出:AddMissingPrimaryKeyOnAnnotationTagMapping1728659839644。关键函数/方法:up、assert。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1728659839644-AddMissingPrimaryKeyOnAnnotationTagMapping.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1728659839644_AddMissingPrimaryKeyOnAnnotationTagMapping.py

import assert from 'node:assert';

import type { IrreversibleMigration, MigrationContext } from '../migration-types';

export class AddMissingPrimaryKeyOnAnnotationTagMapping1728659839644
	implements IrreversibleMigration
{
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		// Check if the primary key already exists
		const table = await queryRunner.getTable(`${tablePrefix}execution_annotation_tags`);

		assert(table, 'execution_annotation_tags table not found');

		const hasPrimaryKey = table.primaryColumns.length > 0;

		if (!hasPrimaryKey) {
			await queryRunner.createPrimaryKey(`${tablePrefix}execution_annotation_tags`, [
				'annotationId',
				'tagId',
			]);
		}
	}
}
