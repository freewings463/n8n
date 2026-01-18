"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/list-query/index.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares/list-query 的入口。导入/依赖:外部:express；内部:@/requests；本地:./filter、./pagination、./select、./sort-by。导出:ListQueryMiddleware、listQueryMiddleware。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/list-query/index.ts -> services/n8n/presentation/cli/api/middleware/list-query/__init__.py

import { type NextFunction, type Response } from 'express';

import type { ListQuery } from '@/requests';

import { filterListQueryMiddleware } from './filter';
import { paginationListQueryMiddleware } from './pagination';
import { selectListQueryMiddleware } from './select';
import { sortByQueryMiddleware } from './sort-by';

export type ListQueryMiddleware = (
	req: ListQuery.Request,
	res: Response,
	next: NextFunction,
) => void;

/**
 * @deprecated Please create Zod validators in `@n8n/api-types` instead.
 */
export const listQueryMiddleware: ListQueryMiddleware[] = [
	filterListQueryMiddleware,
	selectListQueryMiddleware,
	paginationListQueryMiddleware,
	sortByQueryMiddleware,
];
