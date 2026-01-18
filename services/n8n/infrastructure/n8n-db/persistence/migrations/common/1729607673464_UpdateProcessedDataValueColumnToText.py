"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1729607673464-UpdateProcessedDataValueColumnToText.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:UpdateProcessedDataValueColumnToText1729607673464。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1729607673464-UpdateProcessedDataValueColumnToText.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1729607673464_UpdateProcessedDataValueColumnToText.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const processedDataTableName = 'processed_data';
export class UpdateProcessedDataValueColumnToText1729607673464 implements ReversibleMigration {
	async up({ schemaBuilder: { addNotNull }, isMysql, runQuery, tablePrefix }: MigrationContext) {
		const prefixedTableName = `${tablePrefix}${processedDataTableName}`;
		await runQuery(`ALTER TABLE ${prefixedTableName} ADD COLUMN value_temp TEXT;`);
		await runQuery(`UPDATE ${prefixedTableName} SET value_temp = value;`);
		await runQuery(`ALTER TABLE ${prefixedTableName} DROP COLUMN value;`);

		if (isMysql) {
			await runQuery(`ALTER TABLE ${prefixedTableName} CHANGE value_temp value TEXT NOT NULL;`);
		} else {
			await runQuery(`ALTER TABLE ${prefixedTableName} RENAME COLUMN value_temp TO value`);
			await addNotNull(processedDataTableName, 'value');
		}
	}

	async down({ schemaBuilder: { addNotNull }, isMysql, runQuery, tablePrefix }: MigrationContext) {
		const prefixedTableName = `${tablePrefix}${processedDataTableName}`;
		await runQuery(`ALTER TABLE ${prefixedTableName} ADD COLUMN value_temp VARCHAR(255);`);
		await runQuery(`UPDATE ${prefixedTableName} SET value_temp = value;`);
		await runQuery(`ALTER TABLE ${prefixedTableName} DROP COLUMN value;`);

		if (isMysql) {
			await runQuery(
				`ALTER TABLE ${prefixedTableName} CHANGE value_temp value VARCHAR(255) NOT NULL;`,
			);
		} else {
			await runQuery(`ALTER TABLE ${prefixedTableName} RENAME COLUMN value_temp TO value`);
			await addNotNull(processedDataTableName, 'value');
		}
	}
}
