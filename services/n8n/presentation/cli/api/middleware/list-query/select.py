"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/list-query/select.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares/list-query 的模块。导入/依赖:外部:express；内部:@/requests、@/response-helper、@/utils；本地:./dtos/credentials.select.dto、./dtos/user.select.dto、./dtos/workflow.select.dto。导出:selectListQueryMiddleware。关键函数/方法:next。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/list-query/select.ts -> services/n8n/presentation/cli/api/middleware/list-query/select.py

import type { RequestHandler } from 'express';

import type { ListQuery } from '@/requests';
import * as ResponseHelper from '@/response-helper';
import { toError } from '@/utils';

import { CredentialsSelect } from './dtos/credentials.select.dto';
import { UserSelect } from './dtos/user.select.dto';
import { WorkflowSelect } from './dtos/workflow.select.dto';

export const selectListQueryMiddleware: RequestHandler = (req: ListQuery.Request, res, next) => {
	const { select: rawSelect } = req.query;

	if (!rawSelect) return next();

	let Select;

	if (req.baseUrl.endsWith('workflows') || req.path.endsWith('workflows')) {
		Select = WorkflowSelect;
	} else if (req.baseUrl.endsWith('credentials')) {
		Select = CredentialsSelect;
	} else if (req.baseUrl.endsWith('users')) {
		Select = UserSelect;
	} else {
		return next();
	}

	try {
		const select = Select.fromString(rawSelect);

		if (Object.keys(select).length === 0) return next();

		req.listQueryOptions = { ...req.listQueryOptions, select };

		next();
	} catch (maybeError) {
		ResponseHelper.sendErrorResponse(res, toError(maybeError));
	}
};
