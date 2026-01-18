"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/data-table.types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/data-table 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:DataTableUserTableName、columnTypeToFieldType。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/data-table.types.ts -> services/n8n/application/cli/services/modules/data-table/data_table_types.py

import type { FieldTypeMap } from 'n8n-workflow';

export type DataTableUserTableName = `${string}data_table_user_${string}`;

export const columnTypeToFieldType: Record<string, keyof FieldTypeMap> = {
	// eslint-disable-next-line id-denylist
	number: 'number',
	// eslint-disable-next-line id-denylist
	string: 'string',
	// eslint-disable-next-line id-denylist
	boolean: 'boolean',
	date: 'dateTime',
};
