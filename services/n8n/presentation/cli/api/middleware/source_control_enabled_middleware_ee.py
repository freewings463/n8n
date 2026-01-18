"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/middleware/source-control-enabled-middleware.ee.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/source-control.ee/middleware 的中间件。导入/依赖:外部:express；内部:@n8n/di；本地:../source-control-preferences.service.ee。导出:sourceControlEnabledMiddleware。关键函数/方法:next。用于为该模块提供鉴权、拦截、上下文或统一异常处理。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/middleware/source-control-enabled-middleware.ee.ts -> services/n8n/presentation/cli/api/middleware/source_control_enabled_middleware_ee.py

import { Container } from '@n8n/di';
import type { RequestHandler } from 'express';

import { SourceControlPreferencesService } from '../source-control-preferences.service.ee';

export const sourceControlEnabledMiddleware: RequestHandler = (_req, res, next) => {
	const sourceControlPreferencesService = Container.get(SourceControlPreferencesService);

	if (sourceControlPreferencesService.isSourceControlConnected()) {
		next();
	} else {
		res.status(412).json({
			status: 'error',
			message: 'source_control_not_connected',
		});
	}
};
