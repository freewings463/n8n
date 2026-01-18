"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/data-table-filter.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:zod；内部:无；本地:./data-table.schema。导出:FilterConditionSchema、DataTableFilterConditionType、dataTableFilterRecordSchema、dataTableFilterTypeSchema、dataTableFilterSchema、DataTableFilter。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/data-table-filter.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/data_table_filter_schema.py

import { z } from 'zod';

import { dataTableColumnNameSchema } from './data-table.schema';

export const FilterConditionSchema = z.union([
	z.literal('eq'),
	z.literal('neq'),
	z.literal('like'),
	z.literal('ilike'),
	z.literal('gt'),
	z.literal('gte'),
	z.literal('lt'),
	z.literal('lte'),
]);

export type DataTableFilterConditionType = z.infer<typeof FilterConditionSchema>;

export const dataTableFilterRecordSchema = z.object({
	columnName: dataTableColumnNameSchema,
	condition: FilterConditionSchema.default('eq'),
	value: z.union([z.string(), z.number(), z.boolean(), z.date(), z.null()]),
});

export const dataTableFilterTypeSchema = z.union([z.literal('and'), z.literal('or')]);

export const dataTableFilterSchema = z.object({
	type: dataTableFilterTypeSchema.default('and'),
	filters: z.array(dataTableFilterRecordSchema).default([]),
});

export type DataTableFilter = z.infer<typeof dataTableFilterSchema>;
