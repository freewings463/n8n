"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/data-table/list-data-table-content-query.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/data-table 的模块。导入/依赖:外部:zod、zod-class；内部:n8n-workflow；本地:../schemas/data-table-filter.schema、../schemas/data-table.schema、../pagination/pagination.dto。导出:ListDataTableContentQueryDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/data-table/list-data-table-content-query.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/data-table/list_data_table_content_query_dto.py

import { jsonParse } from 'n8n-workflow';
import { z } from 'zod';
import { Z } from 'zod-class';

import { dataTableFilterSchema } from '../../schemas/data-table-filter.schema';
import { dataTableColumnNameSchema } from '../../schemas/data-table.schema';
import { paginationSchema } from '../pagination/pagination.dto';

const filterValidator = z
	.string()
	.optional()
	.transform((val, ctx) => {
		if (!val) return undefined;
		try {
			const parsed: unknown = jsonParse(val);
			try {
				return dataTableFilterSchema.parse(parsed);
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

const sortByValidator = z
	.string()
	.optional()
	.transform((val, ctx) => {
		if (val === undefined) return val;

		if (!val.includes(':')) {
			ctx.addIssue({
				code: z.ZodIssueCode.custom,
				message: 'Invalid sort format, expected <columnName>:<asc/desc>',
				path: ['sort'],
			});
			return z.NEVER;
		}

		let [column, direction] = val.split(':');

		try {
			column = dataTableColumnNameSchema.parse(column);
		} catch {
			ctx.addIssue({
				code: z.ZodIssueCode.custom,
				message: 'Invalid sort columnName',
				path: ['sort'],
			});
			return z.NEVER;
		}

		direction = direction?.toUpperCase();
		if (direction !== 'ASC' && direction !== 'DESC') {
			ctx.addIssue({
				code: z.ZodIssueCode.custom,
				message: 'Invalid sort direction',
				path: ['sort'],
			});

			return z.NEVER;
		}
		return [column, direction] as const;
	});

export class ListDataTableContentQueryDto extends Z.class({
	take: paginationSchema.take.optional(),
	skip: paginationSchema.skip.optional(),
	filter: filterValidator.optional(),
	sortBy: sortByValidator.optional(),
	search: z.string().optional(),
}) {}
