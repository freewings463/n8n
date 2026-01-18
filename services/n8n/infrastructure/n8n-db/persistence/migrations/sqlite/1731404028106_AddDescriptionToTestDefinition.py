"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1731404028106-AddDescriptionToTestDefinition.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../common/1731404028106-AddDescriptionToTestDefinition。导出:AddDescriptionToTestDefinition1731404028106。关键函数/方法:无。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1731404028106-AddDescriptionToTestDefinition.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1731404028106_AddDescriptionToTestDefinition.py

import { AddDescriptionToTestDefinition1731404028106 as BaseMigration } from '../common/1731404028106-AddDescriptionToTestDefinition';

export class AddDescriptionToTestDefinition1731404028106 extends BaseMigration {
	transaction = false as const;
}
