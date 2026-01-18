"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/mcp.auth.consent.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/mcp 的控制器。导入/依赖:外部:express；内部:@n8n/backend-common、@n8n/db、@n8n/decorators；本地:./dto/approve-consent-request.dto、./mcp-oauth-consent.service、./oauth-session.service。导出:McpConsentController。关键函数/方法:getConsentDetails、approveConsent、sendErrorResponse、sendInvalidSessionError、getAndValidateSessionToken。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/mcp.auth.consent.controller.ts -> services/n8n/presentation/cli/api/modules/mcp/mcp_auth_consent_controller.py

import { Logger } from '@n8n/backend-common';
import type { AuthenticatedRequest } from '@n8n/db';
import { Body, Get, Post, RestController } from '@n8n/decorators';
import type { Response } from 'express';

import { ApproveConsentRequestDto } from './dto/approve-consent-request.dto';
import { McpOAuthConsentService } from './mcp-oauth-consent.service';
import { OAuthSessionService } from './oauth-session.service';

@RestController('/consent')
export class McpConsentController {
	constructor(
		private readonly logger: Logger,
		private readonly consentService: McpOAuthConsentService,
		private readonly oauthSessionService: OAuthSessionService,
	) {}

	@Get('/details', { usesTemplates: true })
	async getConsentDetails(req: AuthenticatedRequest, res: Response) {
		try {
			const sessionToken = this.getAndValidateSessionToken(req, res);
			if (!sessionToken) return;

			const consentDetails = await this.consentService.getConsentDetails(sessionToken);

			if (!consentDetails) {
				this.sendInvalidSessionError(res, true);
				return;
			}

			res.json({
				data: {
					clientName: consentDetails.clientName,
					clientId: consentDetails.clientId,
				},
			});
		} catch (error) {
			this.logger.error('Failed to get consent details', { error });
			this.oauthSessionService.clearSession(res);
			this.sendErrorResponse(res, 500, 'Failed to load authorization details');
		}
	}

	@Post('/approve', { usesTemplates: true })
	async approveConsent(
		req: AuthenticatedRequest,
		res: Response,
		@Body payload: ApproveConsentRequestDto,
	) {
		try {
			const sessionToken = this.getAndValidateSessionToken(req, res);
			if (!sessionToken) return;

			const result = await this.consentService.handleConsentDecision(
				sessionToken,
				req.user.id,
				payload.approved,
			);

			this.oauthSessionService.clearSession(res);

			res.json({
				data: {
					status: 'success',
					redirectUrl: result.redirectUrl,
				},
			});
		} catch (error) {
			this.logger.error('Failed to process consent', { error });
			this.oauthSessionService.clearSession(res);
			const message = error instanceof Error ? error.message : 'Failed to process authorization';
			this.sendErrorResponse(res, 500, message);
		}
	}

	private sendErrorResponse(res: Response, statusCode: number, message: string): void {
		res.status(statusCode).json({
			status: 'error',
			message,
		});
	}

	private sendInvalidSessionError(res: Response, clearCookie = false): void {
		if (clearCookie) {
			this.oauthSessionService.clearSession(res);
		}
		this.sendErrorResponse(res, 400, 'Invalid or expired authorization session');
	}

	private getAndValidateSessionToken(req: AuthenticatedRequest, res: Response): string | null {
		const sessionToken = this.oauthSessionService.getSessionToken(req.cookies);
		if (!sessionToken) {
			this.sendInvalidSessionError(res);
			return null;
		}

		try {
			this.oauthSessionService.verifySession(sessionToken);
			return sessionToken;
		} catch (error) {
			this.logger.debug('Invalid session token', { error });
			this.sendInvalidSessionError(res, true);
			return null;
		}
	}
}
