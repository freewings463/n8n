"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/list-query/pagination.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares/list-query 的模块。导入/依赖:外部:express；内部:n8n-workflow、@/requests、@/response-helper、@/utils；本地:./dtos/pagination.dto。导出:paginationListQueryMiddleware。关键函数/方法:next。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/list-query/pagination.ts -> services/n8n/presentation/cli/api/middleware/list-query/pagination.py

import type { RequestHandler } from 'express';
import { UnexpectedError } from 'n8n-workflow';

import type { ListQuery } from '@/requests';
import * as ResponseHelper from '@/response-helper';
import { toError } from '@/utils';

import { Pagination } from './dtos/pagination.dto';

export const paginationListQueryMiddleware: RequestHandler = (
	req: ListQuery.Request,
	res,
	next,
) => {
	const { take: rawTake, skip: rawSkip = '0' } = req.query;

	try {
		if (!rawTake && req.query.skip) {
			throw new UnexpectedError('Please specify `take` when using `skip`');
		}

		if (!rawTake) return next();

		const { take, skip } = Pagination.fromString(rawTake, rawSkip);

		req.listQueryOptions = { ...req.listQueryOptions, skip, take };

		next();
	} catch (maybeError) {
		ResponseHelper.sendErrorResponse(res, toError(maybeError));
	}
};
