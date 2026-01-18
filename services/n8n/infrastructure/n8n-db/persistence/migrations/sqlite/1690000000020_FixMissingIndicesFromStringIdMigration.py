"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1690000000020-FixMissingIndicesFromStringIdMigration.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:FixMissingIndicesFromStringIdMigration1690000000020。关键函数/方法:up、toMerge、tags。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1690000000020-FixMissingIndicesFromStringIdMigration.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1690000000020_FixMissingIndicesFromStringIdMigration.py

import type { IrreversibleMigration, MigrationContext } from '../migration-types';

export class FixMissingIndicesFromStringIdMigration1690000000020 implements IrreversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext): Promise<void> {
		const toMerge = (await queryRunner.query(
			`SELECT id, name, COUNT(*) c FROM ${tablePrefix}tag_entity GROUP BY name HAVING c > 1`,
		)) as Array<{ id: string; name: string }>;

		for (const m of toMerge) {
			const tags = (await queryRunner.query(
				`SELECT id FROM ${tablePrefix}tag_entity WHERE name = ?`,
				[m.name],
			)) as Array<{ id: string }>;
			for (const t of tags) {
				if (t.id === m.id) {
					continue;
				}
				await queryRunner.query(
					`UPDATE ${tablePrefix}workflows_tags SET tagId = ? WHERE tagId = ?`,
					[m.id, t.id],
				);
				await queryRunner.query(`DELETE FROM ${tablePrefix}tag_entity WHERE id = ?`, [t.id]);
			}
		}

		await queryRunner.query(
			`CREATE UNIQUE INDEX "IDX_${tablePrefix}8f949d7a3a984759044054e89b" ON "${tablePrefix}tag_entity" ("name") `,
		);

		await queryRunner.query(
			`CREATE INDEX 'IDX_${tablePrefix}b94b45ce2c73ce46c54f20b5f9' ON '${tablePrefix}execution_entity' ('waitTill', 'id');`,
		);
		await queryRunner.query(
			`CREATE INDEX 'IDX_${tablePrefix}81fc04c8a17de15835713505e4' ON '${tablePrefix}execution_entity' ('workflowId', 'id');`,
		);
		await queryRunner.query(
			`CREATE INDEX 'IDX_${tablePrefix}8b6f3f9ae234f137d707b98f3bf43584' ON '${tablePrefix}execution_entity' ('status', 'workflowId');`,
		);
	}
}
