"""
MIGRATION-META:
  source_path: packages/cli/src/public-api/v1/handlers/audit/audit.handler.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/public-api/v1/handlers 的模块。导入/依赖:外部:express；内部:@n8n/di、@/public-api/types、@/security-audit/security-audit.service；本地:../middlewares/global.middleware。导出:无。关键函数/方法:apiKeyHasScopeWithGlobalScopeFallback、async。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/public-api/v1/handlers/audit/audit.handler.ts -> services/n8n/presentation/cli/api/public-api/v1/handlers/audit/audit_handler.py

import { Container } from '@n8n/di';
import type { Response } from 'express';

import type { AuditRequest } from '@/public-api/types';

import { apiKeyHasScopeWithGlobalScopeFallback } from '../../shared/middlewares/global.middleware';

export = {
	generateAudit: [
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'securityAudit:generate' }),
		async (req: AuditRequest.Generate, res: Response): Promise<Response> => {
			try {
				const { SecurityAuditService } = await import('@/security-audit/security-audit.service');
				const result = await Container.get(SecurityAuditService).run(
					req.body?.additionalOptions?.categories,
					req.body?.additionalOptions?.daysAbandonedWorkflow,
				);

				return res.json(result);
			} catch (error) {
				return res.status(500).json(error);
			}
		},
	],
};
