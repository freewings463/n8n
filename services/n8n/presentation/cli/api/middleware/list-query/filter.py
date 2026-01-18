"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/list-query/filter.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares/list-query 的模块。导入/依赖:外部:express；内部:@/requests、@/response-helper、@/utils；本地:./dtos/credentials.filter.dto、./dtos/user.filter.dto、./dtos/workflow.filter.dto。导出:filterListQueryMiddleware。关键函数/方法:filterListQueryMiddleware、next。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/list-query/filter.ts -> services/n8n/presentation/cli/api/middleware/list-query/filter.py

import type { NextFunction, Response } from 'express';

import type { ListQuery } from '@/requests';
import * as ResponseHelper from '@/response-helper';
import { toError } from '@/utils';

import { CredentialsFilter } from './dtos/credentials.filter.dto';
import { UserFilter } from './dtos/user.filter.dto';
import { WorkflowFilter } from './dtos/workflow.filter.dto';

export const filterListQueryMiddleware = async (
	req: ListQuery.Request,
	res: Response,
	next: NextFunction,
) => {
	const { filter: rawFilter } = req.query;

	if (!rawFilter) return next();

	let Filter;

	if (req.baseUrl.endsWith('workflows') || req.path.endsWith('workflows')) {
		Filter = WorkflowFilter;
	} else if (req.baseUrl.endsWith('credentials')) {
		Filter = CredentialsFilter;
	} else if (req.baseUrl.endsWith('users')) {
		Filter = UserFilter;
	} else {
		return next();
	}

	try {
		const filter = await Filter.fromString(rawFilter);

		if (Object.keys(filter).length === 0) return next();

		req.listQueryOptions = { ...req.listQueryOptions, filter };

		next();
	} catch (maybeError) {
		ResponseHelper.sendErrorResponse(res, toError(maybeError));
	}
};
