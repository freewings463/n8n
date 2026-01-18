"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1669739707126-AddWorkflowVersionIdColumn.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../common/1669739707124-AddWorkflowVersionIdColumn。导出:AddWorkflowVersionIdColumn1669739707126。关键函数/方法:无。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1669739707126-AddWorkflowVersionIdColumn.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1669739707126_AddWorkflowVersionIdColumn.py

import { AddWorkflowVersionIdColumn1669739707124 } from '../common/1669739707124-AddWorkflowVersionIdColumn';

export class AddWorkflowVersionIdColumn1669739707126 extends AddWorkflowVersionIdColumn1669739707124 {}
