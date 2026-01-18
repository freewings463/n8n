"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/mysqldb/1658932910559-AddNodeIds.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/mysqldb 的迁移。导入/依赖:外部:无；内部:无；本地:../common/1658930531669-AddNodeIds。导出:AddNodeIds1658932910559。关键函数/方法:无。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/mysqldb/1658932910559-AddNodeIds.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/mysqldb/1658932910559_AddNodeIds.py

import { AddNodeIds1658930531669 } from '../common/1658930531669-AddNodeIds';

export class AddNodeIds1658932910559 extends AddNodeIds1658930531669 {}
