"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/list-query/sort-by.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares/list-query 的模块。导入/依赖:外部:class-transformer、class-validator、express；内部:n8n-workflow、@/requests、@/response-helper、@/utils；本地:./dtos/workflow.sort-by.dto。导出:sortByQueryMiddleware。关键函数/方法:next。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/list-query/sort-by.ts -> services/n8n/presentation/cli/api/middleware/list-query/sort_by.py

import { plainToInstance } from 'class-transformer';
import { validateSync } from 'class-validator';
import type { RequestHandler } from 'express';
import { UnexpectedError } from 'n8n-workflow';

import type { ListQuery } from '@/requests';
import * as ResponseHelper from '@/response-helper';
import { toError } from '@/utils';

import { WorkflowSorting } from './dtos/workflow.sort-by.dto';

export const sortByQueryMiddleware: RequestHandler = (req: ListQuery.Request, res, next) => {
	const { sortBy } = req.query;

	if (!sortBy) return next();

	let SortBy;

	try {
		if (req.baseUrl.endsWith('workflows') || req.path.endsWith('workflows')) {
			SortBy = WorkflowSorting;
		} else {
			return next();
		}

		const validationResponse = validateSync(plainToInstance(SortBy, { sortBy }));

		if (validationResponse.length) {
			const validationError = validationResponse[0];
			throw new UnexpectedError(validationError.constraints?.workflowSortBy ?? '');
		}

		req.listQueryOptions = { ...req.listQueryOptions, sortBy };

		next();
	} catch (maybeError) {
		ResponseHelper.sendErrorResponse(res, toError(maybeError));
	}
};
