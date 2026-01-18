"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/owner.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的控制器。导入/依赖:外部:express；内部:@n8n/api-types、@n8n/db、@n8n/decorators、@/auth/auth.service、@/posthog、@/services/banner.service 等2项；本地:无。导出:OwnerController。关键函数/方法:setupOwner、dismissBanner。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/owner.controller.ts -> services/n8n/presentation/cli/api/controllers/owner_controller.py

import { DismissBannerRequestDto, OwnerSetupRequestDto } from '@n8n/api-types';
import { AuthenticatedRequest } from '@n8n/db';
import { Body, GlobalScope, Post, RestController } from '@n8n/decorators';
import { Response } from 'express';

import { AuthService } from '@/auth/auth.service';
import { PostHogClient } from '@/posthog';
import { BannerService } from '@/services/banner.service';
import { UserService } from '@/services/user.service';
import { OwnershipService } from '@/services/ownership.service';

@RestController('/owner')
export class OwnerController {
	constructor(
		private readonly authService: AuthService,
		private readonly bannerService: BannerService,
		private readonly userService: UserService,
		private readonly postHog: PostHogClient,
		private readonly ownershipService: OwnershipService,
	) {}

	/**
	 * Promote a shell into the owner of the n8n instance
	 */
	@Post('/setup', { skipAuth: true })
	async setupOwner(req: AuthenticatedRequest, res: Response, @Body payload: OwnerSetupRequestDto) {
		const owner = await this.ownershipService.setupOwner(payload);
		this.authService.issueCookie(res, owner, req.authInfo?.usedMfa ?? false, req.browserId);
		return await this.userService.toPublic(owner, { posthog: this.postHog, withScopes: true });
	}

	@Post('/dismiss-banner')
	@GlobalScope('banner:dismiss')
	async dismissBanner(
		_req: AuthenticatedRequest,
		_res: Response,
		@Body payload: DismissBannerRequestDto,
	) {
		const bannerName = payload.banner;
		if (!bannerName) return;
		await this.bannerService.dismissBanner(bannerName);
	}
}
