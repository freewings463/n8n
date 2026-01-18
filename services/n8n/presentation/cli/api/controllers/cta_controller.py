"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/cta.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的控制器。导入/依赖:外部:express；内部:@n8n/db、@n8n/decorators、@/services/cta.service；本地:无。导出:CtaController。关键函数/方法:getCta。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/cta.controller.ts -> services/n8n/presentation/cli/api/controllers/cta_controller.py

import { AuthenticatedRequest } from '@n8n/db';
import { Get, RestController } from '@n8n/decorators';
import express from 'express';

import { CtaService } from '@/services/cta.service';

/**
 * Controller for Call to Action (CTA) endpoints. CTAs are certain
 * messages that are shown to users in the UI.
 */
@RestController('/cta')
export class CtaController {
	constructor(private readonly ctaService: CtaService) {}

	@Get('/become-creator')
	async getCta(req: AuthenticatedRequest, res: express.Response) {
		const becomeCreator = await this.ctaService.getBecomeCreatorCta(req.user.id);

		res.json(becomeCreator);
	}
}
