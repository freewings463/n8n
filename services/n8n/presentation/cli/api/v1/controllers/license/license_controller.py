"""
MIGRATION-META:
  source_path: packages/cli/src/license/license.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/license 的控制器。导入/依赖:外部:axios；内部:@n8n/api-types、@n8n/db、@n8n/decorators、n8n-core、@/errors/…/bad-request.error、@/requests 等1项；本地:./license.service。导出:LicenseController。关键函数/方法:getLicenseData、requestEnterpriseTrial、registerCommunityEdition、activateLicense、renewLicense、getTokenAndData。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/license/license.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/license/license_controller.py

import { CommunityRegisteredRequestDto } from '@n8n/api-types';
import { AuthenticatedRequest } from '@n8n/db';
import { Get, Post, RestController, GlobalScope, Body } from '@n8n/decorators';
import type { AxiosError } from 'axios';
import { InstanceSettings } from 'n8n-core';

import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import { LicenseRequest } from '@/requests';
import { UrlService } from '@/services/url.service';

import { LicenseService } from './license.service';

@RestController('/license')
export class LicenseController {
	constructor(
		private readonly licenseService: LicenseService,
		private readonly instanceSettings: InstanceSettings,
		private readonly urlService: UrlService,
	) {}

	@Get('/')
	async getLicenseData() {
		return await this.licenseService.getLicenseData();
	}

	@Post('/enterprise/request_trial')
	@GlobalScope('license:manage')
	async requestEnterpriseTrial(req: AuthenticatedRequest) {
		try {
			await this.licenseService.requestEnterpriseTrial(req.user);
		} catch (error: unknown) {
			if (error instanceof Error) {
				const errorMsg =
					(error as AxiosError<{ message: string }>).response?.data?.message ?? error.message;

				throw new BadRequestError(errorMsg);
			} else {
				throw new BadRequestError('Failed to request trial');
			}
		}
	}

	@Post('/enterprise/community-registered')
	async registerCommunityEdition(
		req: AuthenticatedRequest,
		_res: Response,
		@Body payload: CommunityRegisteredRequestDto,
	) {
		return await this.licenseService.registerCommunityEdition({
			userId: req.user.id,
			email: payload.email,
			instanceId: this.instanceSettings.instanceId,
			instanceUrl: this.urlService.getInstanceBaseUrl(),
			licenseType: 'community-registered',
		});
	}

	@Post('/activate')
	@GlobalScope('license:manage')
	async activateLicense(req: LicenseRequest.Activate) {
		const { activationKey, eulaUri } = req.body;
		await this.licenseService.activateLicense(activationKey, eulaUri);
		return await this.getTokenAndData();
	}

	@Post('/renew')
	@GlobalScope('license:manage')
	async renewLicense() {
		await this.licenseService.renewLicense();
		return await this.getTokenAndData();
	}

	private async getTokenAndData() {
		const managementToken = this.licenseService.getManagementJwt();
		const data = await this.licenseService.getLicenseData();
		return { ...data, managementToken };
	}
}
