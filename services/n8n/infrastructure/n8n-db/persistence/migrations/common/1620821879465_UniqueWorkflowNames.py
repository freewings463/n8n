"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1620821879465-UniqueWorkflowNames.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../../entities、../migration-types。导出:UniqueWorkflowNames1620821879465。关键函数/方法:up、down。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1620821879465-UniqueWorkflowNames.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1620821879465_UniqueWorkflowNames.py

import type { WorkflowEntity } from '../../entities';
import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class UniqueWorkflowNames1620821879465 implements ReversibleMigration {
	protected indexSuffix = '943d8f922be094eb507cb9a7f9';

	async up({ isMysql, escape, runQuery }: MigrationContext) {
		const tableName = escape.tableName('workflow_entity');
		const workflowNames: Array<Pick<WorkflowEntity, 'name'>> = await runQuery(
			`SELECT name FROM ${tableName}`,
		);

		for (const { name } of workflowNames) {
			const duplicates: Array<Pick<WorkflowEntity, 'id' | 'name'>> = await runQuery(
				`SELECT id, name FROM ${tableName} WHERE name = :name ORDER BY createdAt ASC`,
				{ name },
			);

			if (duplicates.length > 1) {
				await Promise.all(
					duplicates.map(async (workflow, index) => {
						if (index === 0) return;
						return await runQuery(`UPDATE ${tableName} SET name = :name WHERE id = :id`, {
							name: `${workflow.name} ${index + 1}`,
							id: workflow.id,
						});
					}),
				);
			}
		}

		const indexName = escape.indexName(this.indexSuffix);
		await runQuery(
			isMysql
				? `ALTER TABLE ${tableName} ADD UNIQUE INDEX ${indexName} (${escape.columnName('name')})`
				: `CREATE UNIQUE INDEX ${indexName} ON ${tableName} ("name")`,
		);
	}

	async down({ isMysql, escape, runQuery }: MigrationContext) {
		const tableName = escape.tableName('workflow_entity');
		const indexName = escape.indexName(this.indexSuffix);
		await runQuery(
			isMysql ? `ALTER TABLE ${tableName} DROP INDEX ${indexName}` : `DROP INDEX ${indexName}`,
		);
	}
}
