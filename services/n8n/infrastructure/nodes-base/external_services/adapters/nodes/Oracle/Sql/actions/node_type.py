"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Oracle/Sql/actions/node.type.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Oracle/Sql 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:OracleDBType、OracleDatabaseType、isOracleDBOperation。关键函数/方法:isOracleDBOperation。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Oracle/Sql/actions/node.type.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Oracle/Sql/actions/node_type.py

import type { AllEntities, Entity } from 'n8n-workflow';

type OracleDBMap = {
	database: 'deleteTable' | 'execute' | 'insert' | 'select' | 'update' | 'upsert';
};

export type OracleDBType = AllEntities<OracleDBMap>;

export type OracleDatabaseType = Entity<OracleDBMap, 'database'>;

export function isOracleDBOperation(op: string): op is OracleDBMap['database'] {
	return ['deleteTable', 'execute', 'insert', 'select', 'update', 'upsert'].includes(op);
}
