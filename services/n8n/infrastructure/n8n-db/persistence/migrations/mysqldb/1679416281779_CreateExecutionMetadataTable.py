"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1679416281779-CreateExecutionMetadataTable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的执行迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:CreateExecutionMetadataTable1679416281779。关键函数/方法:up、down。用于定义执行数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1679416281779-CreateExecutionMetadataTable.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1679416281779_CreateExecutionMetadataTable.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class CreateExecutionMetadataTable1679416281779 implements ReversibleMigration {
	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE ${tablePrefix}execution_metadata (
				id int(11) auto_increment NOT NULL PRIMARY KEY,
				executionId int(11) NOT NULL,
				\`key\` TEXT NOT NULL,
				value TEXT NOT NULL,
				CONSTRAINT \`${tablePrefix}execution_metadata_FK\` FOREIGN KEY (\`executionId\`) REFERENCES \`${tablePrefix}execution_entity\` (\`id\`) ON DELETE CASCADE,
				INDEX \`IDX_${tablePrefix}6d44376da6c1058b5e81ed8a154e1fee106046eb\` (\`executionId\` ASC)
			)
			ENGINE=InnoDB`,
		);

		// Remove indices that are no longer needed since the addition of the status column
		await queryRunner.query(
			`DROP INDEX \`IDX_${tablePrefix}06da892aaf92a48e7d3e400003\` ON \`${tablePrefix}execution_entity\``,
		);
		await queryRunner.query(
			`DROP INDEX \`IDX_${tablePrefix}78d62b89dc1433192b86dce18a\` ON \`${tablePrefix}execution_entity\``,
		);
		await queryRunner.query(
			`DROP INDEX \`IDX_${tablePrefix}1688846335d274033e15c846a4\` ON \`${tablePrefix}execution_entity\``,
		);
		await queryRunner.query(
			`DROP INDEX \`IDX_${tablePrefix}cefb067df2402f6aed0638a6c1\` ON \`${tablePrefix}execution_entity\``,
		);

		// Add index to the new status column
		await queryRunner.query(
			`CREATE INDEX \`IDX_${tablePrefix}8b6f3f9ae234f137d707b98f3bf43584\` ON \`${tablePrefix}execution_entity\` (\`status\`, \`workflowId\`)`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`DROP TABLE "${tablePrefix}execution_metadata"`);
		await queryRunner.query(
			`CREATE INDEX \`IDX_${tablePrefix}06da892aaf92a48e7d3e400003\` ON \`${tablePrefix}execution_entity\` (\`workflowId\`, \`waitTill\`, \`id\`)`,
		);
		await queryRunner.query(
			`CREATE INDEX \`IDX_${tablePrefix}78d62b89dc1433192b86dce18a\` ON \`${tablePrefix}execution_entity\` (\`workflowId\`, \`finished\`, \`id\`)`,
		);
		await queryRunner.query(
			`CREATE INDEX \`IDX_${tablePrefix}1688846335d274033e15c846a4\` ON \`${tablePrefix}execution_entity\` (\`finished\`, \`id\`)`,
		);
		await queryRunner.query(
			'CREATE INDEX `IDX_' +
				tablePrefix +
				'cefb067df2402f6aed0638a6c1` ON `' +
				tablePrefix +
				'execution_entity` (`stoppedAt`)',
		);
		await queryRunner.query(
			`DROP INDEX \`IDX_${tablePrefix}8b6f3f9ae234f137d707b98f3bf43584\` ON \`${tablePrefix}execution_entity\``,
		);
	}
}
