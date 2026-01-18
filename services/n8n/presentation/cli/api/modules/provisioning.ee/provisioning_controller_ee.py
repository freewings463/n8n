"""
MIGRATION-META:
  source_path: packages/cli/src/modules/provisioning.ee/provisioning.controller.ee.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/provisioning.ee 的控制器。导入/依赖:外部:express；内部:@n8n/db、@n8n/decorators、@n8n/backend-common；本地:./provisioning.service.ee。导出:ProvisioningController。关键函数/方法:getConfig、patchConfig。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/provisioning.ee/provisioning.controller.ee.ts -> services/n8n/presentation/cli/api/modules/provisioning.ee/provisioning_controller_ee.py

import { AuthenticatedRequest } from '@n8n/db';
import { Get, GlobalScope, Patch, RestController } from '@n8n/decorators';
import { LicenseState } from '@n8n/backend-common';
import { ProvisioningService } from './provisioning.service.ee';
import { Response } from 'express';

@RestController('/sso/provisioning')
export class ProvisioningController {
	constructor(
		private readonly provisioningService: ProvisioningService,
		private readonly licenseState: LicenseState,
	) {}

	@Get('/config')
	@GlobalScope('provisioning:manage')
	async getConfig(_req: AuthenticatedRequest, res: Response) {
		if (!this.licenseState.isProvisioningLicensed()) {
			return res.status(403).json({ message: 'Provisioning is not licensed' });
		}

		return await this.provisioningService.getConfig();
	}

	@Patch('/config')
	@GlobalScope('provisioning:manage')
	async patchConfig(req: AuthenticatedRequest, res: Response) {
		if (!this.licenseState.isProvisioningLicensed()) {
			return res.status(403).json({ message: 'Provisioning is not licensed' });
		}

		return await this.provisioningService.patchConfig(req.body);
	}
}
