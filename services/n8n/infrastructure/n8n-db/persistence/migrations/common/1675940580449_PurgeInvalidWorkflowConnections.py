"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1675940580449-PurgeInvalidWorkflowConnections.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的工作流迁移。导入/依赖:外部:无；内部:n8n-workflow；本地:../../entities、../migration-types。导出:PurgeInvalidWorkflowConnections1675940580449。关键函数/方法:up。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1675940580449-PurgeInvalidWorkflowConnections.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1675940580449_PurgeInvalidWorkflowConnections.py

import { UserError } from 'n8n-workflow';

import { WorkflowEntity } from '../../entities';
import type { IrreversibleMigration, MigrationContext } from '../migration-types';

export class PurgeInvalidWorkflowConnections1675940580449 implements IrreversibleMigration {
	async up({ queryRunner }: MigrationContext) {
		const workflowCount = await queryRunner.manager.count(WorkflowEntity);

		if (workflowCount > 0) {
			throw new UserError(
				'Migration "PurgeInvalidWorkflowConnections1675940580449" is no longer supported. Please upgrade to n8n@1.0.0 first.',
			);
		}
	}
}
