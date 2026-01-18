"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/mcp-oauth-consent.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/mcp 的OAuth服务。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/di、n8n-workflow；本地:../repositories/oauth-client.repository、../repositories/oauth-user-consent.repository、./mcp-oauth-authorization-code.service、./mcp-oauth.helpers 等1项。导出:McpOAuthConsentService。关键函数/方法:getConsentDetails、handleConsentDecision。用于封装OAuth业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/mcp-oauth-consent.service.ts -> services/n8n/application/cli/services/mcp/mcp_oauth_consent_service.py

import { Logger } from '@n8n/backend-common';
import { Service } from '@n8n/di';
import { UserError } from 'n8n-workflow';

import { OAuthClientRepository } from './database/repositories/oauth-client.repository';
import { UserConsentRepository } from './database/repositories/oauth-user-consent.repository';
import { McpOAuthAuthorizationCodeService } from './mcp-oauth-authorization-code.service';
import { McpOAuthHelpers } from './mcp-oauth.helpers';
import { OAuthSessionService, type OAuthSessionPayload } from './oauth-session.service';

/**
 * Manages OAuth consent flow for MCP server
 * Handles user authorization decisions and generates authorization codes
 */
@Service()
export class McpOAuthConsentService {
	constructor(
		private readonly logger: Logger,
		private readonly oauthSessionService: OAuthSessionService,
		private readonly oauthClientRepository: OAuthClientRepository,
		private readonly userConsentRepository: UserConsentRepository,
		private readonly authorizationCodeService: McpOAuthAuthorizationCodeService,
	) {}

	/**
	 * Get consent details from session cookie
	 * Verifies JWT session token and returns client information
	 */
	async getConsentDetails(sessionToken: string): Promise<{
		clientName: string;
		clientId: string;
	} | null> {
		try {
			const sessionPayload = this.oauthSessionService.verifySession(sessionToken);

			const client = await this.oauthClientRepository.findOne({
				where: { id: sessionPayload.clientId },
			});

			if (!client) {
				return null;
			}

			return {
				clientName: client.name,
				clientId: client.id,
			};
		} catch (error) {
			this.logger.error('Error getting consent details', { error });
			return null;
		}
	}

	/**
	 * Handle consent approval/denial
	 * Uses JWT session token instead of database lookup
	 */
	async handleConsentDecision(
		sessionToken: string,
		userId: string,
		approved: boolean,
	): Promise<{ redirectUrl: string }> {
		let sessionPayload: OAuthSessionPayload;
		try {
			sessionPayload = this.oauthSessionService.verifySession(sessionToken);
		} catch (error) {
			throw new UserError('Invalid or expired session');
		}

		if (!approved) {
			const redirectUrl = McpOAuthHelpers.buildErrorRedirectUrl(
				sessionPayload.redirectUri,
				'access_denied',
				'User denied the authorization request',
				sessionPayload.state,
			);

			this.logger.info('Consent denied', {
				clientId: sessionPayload.clientId,
				userId,
			});

			return { redirectUrl };
		}

		await this.userConsentRepository.insert({
			userId,
			clientId: sessionPayload.clientId,
			grantedAt: Date.now(),
		});

		const code = await this.authorizationCodeService.createAuthorizationCode(
			sessionPayload.clientId,
			userId,
			sessionPayload.redirectUri,
			sessionPayload.codeChallenge,
			sessionPayload.state,
		);

		const successRedirectUrl = McpOAuthHelpers.buildSuccessRedirectUrl(
			sessionPayload.redirectUri,
			code,
			sessionPayload.state,
		);

		this.logger.info('Consent approved', {
			clientId: sessionPayload.clientId,
			userId,
		});

		return { redirectUrl: successRedirectUrl };
	}
}
