"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1765459448000-AddResolvableFieldsToCredentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddResolvableFieldsToCredentials1765459448000。关键函数/方法:up、column、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1765459448000-AddResolvableFieldsToCredentials.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1765459448000_AddResolvableFieldsToCredentials.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

const credentialsTableName = 'credentials_entity';
const resolverTableName = 'dynamic_credential_resolver';
const FOREIGN_KEY_NAME = 'credentials_entity_resolverId_foreign';

export class AddResolvableFieldsToCredentials1765459448000 implements ReversibleMigration {
	async up({ schemaBuilder: { addColumns, addForeignKey, column } }: MigrationContext) {
		await addColumns(credentialsTableName, [
			column('isResolvable').bool.notNull.default(false),
			column('resolvableAllowFallback').bool.notNull.default(false),
			column('resolverId').varchar(16),
		]);

		await addForeignKey(
			credentialsTableName,
			'resolverId',
			[resolverTableName, 'id'],
			FOREIGN_KEY_NAME,
			'SET NULL',
		);
	}

	async down({ schemaBuilder: { dropColumns, dropForeignKey } }: MigrationContext) {
		await dropForeignKey(
			credentialsTableName,
			'resolverId',
			[resolverTableName, 'id'],
			FOREIGN_KEY_NAME,
		);

		await dropColumns(credentialsTableName, [
			'isResolvable',
			'resolvableAllowFallback',
			'resolverId',
		]);
	}
}
