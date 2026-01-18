"""
MIGRATION-META:
  source_path: packages/cli/src/sso.ee/oidc/routes/oidc.controller.ee.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/sso.ee/oidc/routes 的SSO控制器。导入/依赖:外部:express；内部:@n8n/api-types、@n8n/backend-common、@n8n/config、@n8n/constants、@n8n/db、@n8n/decorators 等5项；本地:../constants、../oidc.service.ee。导出:OidcController。关键函数/方法:retrieveConfiguration、saveConfiguration、redirectToAuthProvider、callbackHandler。用于处理SSO接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/sso.ee/oidc/routes/oidc.controller.ee.ts -> services/n8n/presentation/cli/api/sso.ee/oidc/routes/oidc_controller_ee.py

import { OidcConfigDto } from '@n8n/api-types';
import { Logger } from '@n8n/backend-common';
import { GlobalConfig } from '@n8n/config';
import { Time } from '@n8n/constants';
import { AuthenticatedRequest } from '@n8n/db';
import { Body, Get, GlobalScope, Licensed, Post, RestController } from '@n8n/decorators';
import { Request, Response } from 'express';

import { AuthService } from '@/auth/auth.service';
import { OIDC_NONCE_COOKIE_NAME, OIDC_STATE_COOKIE_NAME } from '@/constants';
import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import { AuthlessRequest } from '@/requests';
import { UrlService } from '@/services/url.service';

import { OIDC_CLIENT_SECRET_REDACTED_VALUE } from '../constants';
import { OidcService } from '../oidc.service.ee';

@RestController('/sso/oidc')
export class OidcController {
	constructor(
		private readonly oidcService: OidcService,
		private readonly authService: AuthService,
		private readonly urlService: UrlService,
		private readonly globalConfig: GlobalConfig,
		private readonly logger: Logger,
	) {}

	@Get('/config')
	@Licensed('feat:oidc')
	@GlobalScope('oidc:manage')
	async retrieveConfiguration(_req: AuthenticatedRequest) {
		const config = await this.oidcService.loadConfig();
		if (config.clientSecret) {
			config.clientSecret = OIDC_CLIENT_SECRET_REDACTED_VALUE;
		}
		return config;
	}

	@Post('/config')
	@Licensed('feat:oidc')
	@GlobalScope('oidc:manage')
	async saveConfiguration(
		_req: AuthenticatedRequest,
		_res: Response,
		@Body payload: OidcConfigDto,
	) {
		await this.oidcService.updateConfig(payload);
		const config = this.oidcService.getRedactedConfig();
		return config;
	}

	@Get('/login', { skipAuth: true })
	@Licensed('feat:oidc')
	async redirectToAuthProvider(_req: Request, res: Response) {
		const authorization = await this.oidcService.generateLoginUrl();
		const { samesite, secure } = this.globalConfig.auth.cookie;

		res.cookie(OIDC_STATE_COOKIE_NAME, authorization.state, {
			maxAge: 15 * Time.minutes.toMilliseconds,
			httpOnly: true,
			sameSite: samesite,
			secure,
		});
		res.cookie(OIDC_NONCE_COOKIE_NAME, authorization.nonce, {
			maxAge: 15 * Time.minutes.toMilliseconds,
			httpOnly: true,
			sameSite: samesite,
			secure,
		});
		res.redirect(authorization.url.toString());
	}

	@Get('/callback', { skipAuth: true })
	@Licensed('feat:oidc')
	async callbackHandler(req: AuthlessRequest, res: Response) {
		const fullUrl = `${this.urlService.getInstanceBaseUrl()}${req.originalUrl}`;
		const callbackUrl = new URL(fullUrl);
		const state = req.cookies[OIDC_STATE_COOKIE_NAME];

		if (typeof state !== 'string') {
			this.logger.error('State is missing');
			throw new BadRequestError('Invalid state');
		}

		const nonce = req.cookies[OIDC_NONCE_COOKIE_NAME];

		if (typeof nonce !== 'string') {
			this.logger.error('Nonce is missing');
			throw new BadRequestError('Invalid nonce');
		}

		const user = await this.oidcService.loginUser(callbackUrl, state, nonce);

		res.clearCookie(OIDC_STATE_COOKIE_NAME);
		res.clearCookie(OIDC_NONCE_COOKIE_NAME);
		this.authService.issueCookie(res, user, true, req.browserId);

		res.redirect('/');
	}
}
