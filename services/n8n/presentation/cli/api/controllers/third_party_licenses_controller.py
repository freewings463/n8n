"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/third-party-licenses.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的控制器。导入/依赖:外部:express、fs/promises；内部:@/constants、@n8n/decorators；本地:无。导出:ThirdPartyLicensesController。关键函数/方法:getThirdPartyLicenses。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/third-party-licenses.controller.ts -> services/n8n/presentation/cli/api/controllers/third_party_licenses_controller.py

import { CLI_DIR } from '@/constants';
import { Get, RestController } from '@n8n/decorators';
import { Request, Response } from 'express';
import { readFile } from 'fs/promises';
import { resolve } from 'path';

@RestController('/third-party-licenses')
export class ThirdPartyLicensesController {
	/**
	 * Get third-party licenses content
	 * Requires authentication to access
	 */
	@Get('/')
	async getThirdPartyLicenses(_: Request, res: Response) {
		const licenseFile = resolve(CLI_DIR, 'THIRD_PARTY_LICENSES.md');

		try {
			const content = await readFile(licenseFile, 'utf-8');
			res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
			res.send(content);
		} catch {
			res.status(404).send('Third-party licenses file not found');
		}
	}
}
