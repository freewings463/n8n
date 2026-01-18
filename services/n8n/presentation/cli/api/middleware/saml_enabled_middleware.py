"""
MIGRATION-META:
  source_path: packages/cli/src/sso.ee/saml/middleware/saml-enabled-middleware.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/sso.ee/saml/middleware 的SSO中间件。导入/依赖:外部:express；内部:无；本地:../saml-helpers。导出:samlLicensedAndEnabledMiddleware、samlLicensedMiddleware。关键函数/方法:next。用于为SSO提供鉴权、拦截、上下文或统一异常处理。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/sso.ee/saml/middleware/saml-enabled-middleware.ts -> services/n8n/presentation/cli/api/middleware/saml_enabled_middleware.py

import type { RequestHandler } from 'express';

import { isSamlLicensed, isSamlLicensedAndEnabled } from '../saml-helpers';

export const samlLicensedAndEnabledMiddleware: RequestHandler = (_, res, next) => {
	if (isSamlLicensedAndEnabled()) {
		next();
	} else {
		res.status(403).json({ status: 'error', message: 'Unauthorized' });
	}
};

export const samlLicensedMiddleware: RequestHandler = (_, res, next) => {
	if (isSamlLicensed()) {
		next();
	} else {
		res.status(403).json({ status: 'error', message: 'Unauthorized' });
	}
};
