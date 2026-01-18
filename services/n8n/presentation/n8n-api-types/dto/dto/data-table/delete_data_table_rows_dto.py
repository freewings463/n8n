"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/data-table/delete-data-table-rows.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/data-table 的模块。导入/依赖:外部:zod、zod-class；内部:n8n-workflow；本地:../schemas/data-table-filter.schema。导出:DeleteDataTableRowsDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/data-table/delete-data-table-rows.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/data-table/delete_data_table_rows_dto.py

import { jsonParse } from 'n8n-workflow';
import { z } from 'zod';
import { Z } from 'zod-class';

import { dataTableFilterSchema } from '../../schemas/data-table-filter.schema';

const dataTableFilterQueryValidator = z.string().transform((val, ctx) => {
	if (!val) {
		ctx.addIssue({
			code: z.ZodIssueCode.custom,
			message: 'Filter is required for delete operations',
			path: ['filter'],
		});
		return z.NEVER;
	}
	try {
		const parsed: unknown = jsonParse(val);
		try {
			// Parse with the schema which applies defaults
			const result = dataTableFilterSchema.parse(parsed);
			// Ensure filters array is not empty
			if (!result.filters || result.filters.length === 0) {
				ctx.addIssue({
					code: z.ZodIssueCode.custom,
					message: 'At least one filter condition is required for delete operations',
					path: ['filter'],
				});
				return z.NEVER;
			}
			return result;
		} catch (e) {
			ctx.addIssue({
				code: z.ZodIssueCode.custom,
				message: 'Invalid filter fields',
				path: ['filter'],
			});
			return z.NEVER;
		}
	} catch (e) {
		ctx.addIssue({
			code: z.ZodIssueCode.custom,
			message: 'Invalid filter format',
			path: ['filter'],
		});
		return z.NEVER;
	}
});

const booleanValidator = z
	.union([z.string(), z.boolean()])
	.optional()
	.transform((val) => {
		if (typeof val === 'string') {
			return val === 'true';
		}
		return val ?? false;
	});

const deleteDataTableRowsShape = {
	filter: dataTableFilterQueryValidator,
	returnData: booleanValidator,
	dryRun: booleanValidator,
};

export class DeleteDataTableRowsDto extends Z.class(deleteDataTableRowsShape) {}
