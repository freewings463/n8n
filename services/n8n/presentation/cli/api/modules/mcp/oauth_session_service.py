"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/oauth-session.service.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/mcp 的OAuth服务。导入/依赖:外部:express；内部:@n8n/constants、@n8n/di、@/services/jwt.service；本地:无。导出:OAuthSessionPayload、OAuthSessionService。关键函数/方法:createSession、verifySession、clearSession、getSessionToken。用于封装OAuth业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/oauth-session.service.ts -> services/n8n/presentation/cli/api/modules/mcp/oauth_session_service.py

import { Time } from '@n8n/constants';
import { Service } from '@n8n/di';
import { Response } from 'express';

import { JwtService } from '@/services/jwt.service';

export interface OAuthSessionPayload {
	clientId: string;
	redirectUri: string;
	codeChallenge: string;
	state: string | null;
}

const COOKIE_NAME = 'n8n-oauth-session';
const SESSION_EXPIRY_MS = 10 * Time.minutes.toMilliseconds; // 10 minutes

/**
 * Manages OAuth authorization session state using JWT-based cookies
 * Stores temporary session data during the authorization flow
 */
@Service()
export class OAuthSessionService {
	constructor(private readonly jwtService: JwtService) {}

	/**
	 * Create OAuth session token and set it as a cookie
	 */
	createSession(res: Response, payload: OAuthSessionPayload): void {
		const sessionToken = this.jwtService.sign(payload, {
			expiresIn: '10m',
		});

		res.cookie(COOKIE_NAME, sessionToken, {
			httpOnly: true,
			secure: process.env.NODE_ENV === 'production',
			sameSite: 'lax',
			maxAge: SESSION_EXPIRY_MS,
		});
	}

	/**
	 * Verify and decode OAuth session token
	 */
	verifySession(sessionToken: string): OAuthSessionPayload {
		return this.jwtService.verify<OAuthSessionPayload>(sessionToken);
	}

	/**
	 * Clear OAuth session cookie
	 */
	clearSession(res: Response): void {
		res.clearCookie(COOKIE_NAME);
	}

	/**
	 * Extract session token from request cookies
	 */
	getSessionToken(cookies: Record<string, string | undefined>): string | undefined {
		return cookies[COOKIE_NAME];
	}
}
