"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/cors.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares 的模块。导入/依赖:外部:express；内部:无；本地:无。导出:corsMiddleware。关键函数/方法:next。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/cors.ts -> services/n8n/presentation/cli/api/middleware/cors.py

import type { RequestHandler } from 'express';

export const corsMiddleware: RequestHandler = (req, res, next) => {
	if ('origin' in req.headers) {
		// Allow access also from frontend when developing
		res.header('Access-Control-Allow-Origin', req.headers.origin);
		res.header('Access-Control-Allow-Credentials', 'true');
		res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
		res.header(
			'Access-Control-Allow-Headers',
			'Origin, X-Requested-With, Content-Type, Accept, push-ref, browser-id, anonymousid, authorization',
		);
	}

	if (req.method === 'OPTIONS') {
		res.writeHead(204).end();
	} else {
		next();
	}
};
