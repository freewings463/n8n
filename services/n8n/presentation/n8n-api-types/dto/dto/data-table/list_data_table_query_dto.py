"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/data-table/list-data-table-query.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/data-table 的模块。导入/依赖:外部:zod、zod-class；内部:n8n-workflow；本地:../pagination/pagination.dto。导出:ListDataTableQuerySortOptions、ListDataTableQueryDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/data-table/list-data-table-query.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/data-table/list_data_table_query_dto.py

import { jsonParse } from 'n8n-workflow';
import { z } from 'zod';
import { Z } from 'zod-class';

import { paginationSchema } from '../pagination/pagination.dto';

const VALID_SORT_OPTIONS = [
	'name:asc',
	'name:desc',
	'createdAt:asc',
	'createdAt:desc',
	'updatedAt:asc',
	'updatedAt:desc',
	'sizeBytes:asc',
	'sizeBytes:desc',
] as const;

export type ListDataTableQuerySortOptions = (typeof VALID_SORT_OPTIONS)[number];

const FILTER_OPTIONS = {
	id: z.union([z.string(), z.array(z.string())]).optional(),
	name: z.union([z.string(), z.array(z.string())]).optional(),
	projectId: z.union([z.string(), z.array(z.string())]).optional(),
	// todo: can probably include others here as well?
};

// Filter schema - only allow specific properties
const filterSchema = z.object(FILTER_OPTIONS).strict();
// ---------------------
// Parameter Validators
// ---------------------

// Filter parameter validation
const filterValidator = z
	.string()
	.optional()
	.transform((val, ctx) => {
		if (!val) return undefined;
		try {
			const parsed: unknown = jsonParse(val);
			try {
				return filterSchema.parse(parsed);
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

// SortBy parameter validation
const sortByValidator = z
	.enum(VALID_SORT_OPTIONS, { message: `sortBy must be one of: ${VALID_SORT_OPTIONS.join(', ')}` })
	.optional();

export class ListDataTableQueryDto extends Z.class({
	...paginationSchema,
	filter: filterValidator,
	sortBy: sortByValidator,
}) {}
