"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/list-query/dtos/pagination.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares/list-query/dtos 的模块。导入/依赖:外部:无；内部:n8n-workflow、@/utils；本地:无。导出:Pagination。关键函数/方法:fromString。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Middleware -> presentation/api/middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/list-query/dtos/pagination.dto.ts -> services/n8n/presentation/cli/api/middleware/list-query/dtos/pagination_dto.py

import { UnexpectedError } from 'n8n-workflow';

import { isIntegerString } from '@/utils';

export class Pagination {
	static fromString(rawTake: string, rawSkip: string) {
		if (!isIntegerString(rawTake)) {
			throw new UnexpectedError('Parameter take is not an integer string');
		}

		if (!isIntegerString(rawSkip)) {
			throw new UnexpectedError('Parameter skip is not an integer string');
		}

		const [take, skip] = [rawTake, rawSkip].map((o) => parseInt(o, 10));

		const MAX_ITEMS_PER_PAGE = 50;

		return {
			take: Math.min(take, MAX_ITEMS_PER_PAGE),
			skip,
		};
	}
}
