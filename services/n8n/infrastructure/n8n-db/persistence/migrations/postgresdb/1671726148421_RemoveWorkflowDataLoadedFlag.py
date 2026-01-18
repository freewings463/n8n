"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1671726148421-RemoveWorkflowDataLoadedFlag.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的工作流迁移。导入/依赖:外部:无；内部:无；本地:../common/1671726148419-RemoveWorkflowDataLoadedFlag。导出:RemoveWorkflowDataLoadedFlag1671726148421。关键函数/方法:无。用于定义工作流数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1671726148421-RemoveWorkflowDataLoadedFlag.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1671726148421_RemoveWorkflowDataLoadedFlag.py

import { RemoveWorkflowDataLoadedFlag1671726148419 } from '../common/1671726148419-RemoveWorkflowDataLoadedFlag';

export class RemoveWorkflowDataLoadedFlag1671726148421 extends RemoveWorkflowDataLoadedFlag1671726148419 {}
