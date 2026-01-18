"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/postgresdb/1659902242948-AddJsonKeyPinData.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/postgresdb 的迁移。导入/依赖:外部:无；内部:无；本地:../common/1659888469333-AddJsonKeyPinData。导出:AddJsonKeyPinData1659902242948。关键函数/方法:无。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/postgresdb/1659902242948-AddJsonKeyPinData.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/postgresdb/1659902242948_AddJsonKeyPinData.py

import { AddJsonKeyPinData1659888469333 } from '../common/1659888469333-AddJsonKeyPinData';

export class AddJsonKeyPinData1659902242948 extends AddJsonKeyPinData1659888469333 {}
