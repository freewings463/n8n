"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/folders/list-folder-query.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/folders 的模块。导入/依赖:外部:zod、zod-class；内部:n8n-workflow；本地:无。导出:filterSchema、ListFolderQueryDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/folders/list-folder-query.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/folders/list_folder_query_dto.py

import { jsonParse } from 'n8n-workflow';
import { z } from 'zod';
import { Z } from 'zod-class';

const VALID_SELECT_FIELDS = [
	'id',
	'name',
	'createdAt',
	'updatedAt',
	'project',
	'tags',
	'parentFolder',
	'workflowCount',
	'subFolderCount',
	'path',
] as const;

const VALID_SORT_OPTIONS = [
	'name:asc',
	'name:desc',
	'createdAt:asc',
	'createdAt:desc',
	'updatedAt:asc',
	'updatedAt:desc',
] as const;

// Filter schema - only allow specific properties
export const filterSchema = z
	.object({
		parentFolderId: z.string().optional(),
		name: z.string().optional(),
		tags: z.array(z.string()).optional(),
		excludeFolderIdAndDescendants: z.string().optional(),
	})
	.strict();

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

// Skip parameter validation
const skipValidator = z
	.string()
	.optional()
	.transform((val) => (val ? parseInt(val, 10) : 0))
	.refine((val) => !isNaN(val), {
		message: 'Skip must be a valid number',
	});

// Take parameter validation
const takeValidator = z
	.string()
	.optional()
	.transform((val) => (val ? parseInt(val, 10) : 10))
	.refine((val) => !isNaN(val), {
		message: 'Take must be a valid number',
	});

// Select parameter validation
const selectFieldsValidator = z.array(z.enum(VALID_SELECT_FIELDS));
const selectValidator = z
	.string()
	.optional()
	.transform((val, ctx) => {
		if (!val) return undefined;
		try {
			const parsed: unknown = JSON.parse(val);
			try {
				const selectFields = selectFieldsValidator.parse(parsed);
				if (selectFields.length === 0) return undefined;
				type SelectField = (typeof VALID_SELECT_FIELDS)[number];
				return selectFields.reduce<Record<SelectField, true>>(
					(acc, field) => ({ ...acc, [field]: true }),
					{} as Record<SelectField, true>,
				);
			} catch (e) {
				ctx.addIssue({
					code: z.ZodIssueCode.custom,
					message: `Invalid select fields. Valid fields are: ${VALID_SELECT_FIELDS.join(', ')}`,
					path: ['select'],
				});
				return z.NEVER;
			}
		} catch (e) {
			ctx.addIssue({
				code: z.ZodIssueCode.custom,
				message: 'Invalid select format',
				path: ['select'],
			});
			return z.NEVER;
		}
	});

// SortBy parameter validation
const sortByValidator = z
	.enum(VALID_SORT_OPTIONS, { message: `sortBy must be one of: ${VALID_SORT_OPTIONS.join(', ')}` })
	.optional();

export class ListFolderQueryDto extends Z.class({
	filter: filterValidator,
	skip: skipValidator,
	take: takeValidator,
	select: selectValidator,
	sortBy: sortByValidator,
}) {}
