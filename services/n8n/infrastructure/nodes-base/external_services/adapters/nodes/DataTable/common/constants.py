"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DataTable/common/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DataTable/common 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ANY_CONDITION、ALL_CONDITIONS、ROWS_LIMIT_DEFAULT、FilterType、FieldEntry。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DataTable/common/constants.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DataTable/common/constants.py

import type { DataTableColumnJsType } from 'n8n-workflow';

export const ANY_CONDITION = 'anyCondition';
export const ALL_CONDITIONS = 'allConditions';

export const ROWS_LIMIT_DEFAULT = 50;

export type FilterType = typeof ANY_CONDITION | typeof ALL_CONDITIONS;

export type FieldEntry =
	| {
			keyName: string;
			condition: 'isEmpty' | 'isNotEmpty' | 'isTrue' | 'isFalse';
	  }
	| {
			keyName: string;
			condition?: 'eq' | 'neq' | 'like' | 'ilike' | 'gt' | 'gte' | 'lt' | 'lte';
			keyValue: DataTableColumnJsType;
	  };
