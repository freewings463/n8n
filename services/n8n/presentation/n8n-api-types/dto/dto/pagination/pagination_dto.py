"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/pagination/pagination.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/pagination 的模块。导入/依赖:外部:zod、zod-class；内部:无；本地:无。导出:MAX_ITEMS_PER_PAGE、createTakeValidator、paginationSchema、PaginationDto。关键函数/方法:createTakeValidator。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/pagination/pagination.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/pagination/pagination_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

export const MAX_ITEMS_PER_PAGE = 50;

const skipValidator = z
	.string()
	.optional()
	.transform((val) => (val ? parseInt(val, 10) : 0))
	.refine((val) => !isNaN(val) && Number.isInteger(val), {
		message: 'Param `skip` must be a valid integer',
	})
	.refine((val) => val >= 0, {
		message: 'Param `skip` must be a non-negative integer',
	});

export const createTakeValidator = (maxItems: number, allowInfinity: boolean = false) =>
	z
		.string()
		.optional()
		.transform((val) => (val ? parseInt(val, 10) : 10))
		.refine((val) => !isNaN(val) && Number.isInteger(val), {
			message: 'Param `take` must be a valid integer',
		})
		.refine(
			(val) => {
				if (!allowInfinity) return val >= 0;
				return true;
			},
			{
				message: 'Param `take` must be a non-negative integer',
			},
		)
		.transform((val) => Math.min(val, maxItems));

export const paginationSchema = {
	skip: skipValidator,
	take: createTakeValidator(MAX_ITEMS_PER_PAGE),
};

export class PaginationDto extends Z.class(paginationSchema) {}
