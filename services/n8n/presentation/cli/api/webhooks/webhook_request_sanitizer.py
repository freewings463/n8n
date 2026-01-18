"""
MIGRATION-META:
  source_path: packages/cli/src/webhooks/webhook-request-sanitizer.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/webhooks 的Webhook模块。导入/依赖:外部:express；内部:@/constants；本地:无。导出:sanitizeWebhookRequest。关键函数/方法:removeCookiesFromHeader、removeCookiesFromParsedCookies、sanitizeWebhookRequest。用于承载Webhook实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/webhooks/webhook-request-sanitizer.ts -> services/n8n/presentation/cli/api/webhooks/webhook_request_sanitizer.py

import type { Request } from 'express';

import { AUTH_COOKIE_NAME } from '@/constants';

const BROWSER_ID_COOKIE_NAME = 'n8n-browserId';

const DISALLOWED_COOKIES = new Set([AUTH_COOKIE_NAME, BROWSER_ID_COOKIE_NAME]);

/**
 * Removes a cookie with the given name from the request header
 */
const removeCookiesFromHeader = (req: Request) => {
	const cookiesHeader = req.headers.cookie;
	if (typeof cookiesHeader !== 'string') {
		return;
	}

	const cookies = cookiesHeader.split(';').map((cookie) => cookie.trim());
	const filteredCookies = cookies.filter((cookie) => {
		const cookieName = cookie.split('=')[0];
		return !DISALLOWED_COOKIES.has(cookieName);
	});

	if (filteredCookies.length !== cookies.length) {
		req.headers.cookie = filteredCookies.join('; ');
	}
};

/**
 * Removes a cookie with the given name from the parsed cookies object
 */
const removeCookiesFromParsedCookies = (req: Request) => {
	if (req.cookies !== null && typeof req.cookies === 'object') {
		for (const cookieName of DISALLOWED_COOKIES) {
			delete req.cookies[cookieName];
		}
	}
};

export const sanitizeWebhookRequest = (req: Request) => {
	removeCookiesFromHeader(req);
	removeCookiesFromParsedCookies(req);
};
