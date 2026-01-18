"""
MIGRATION-META:
  source_path: packages/@n8n/client-oauth2/src/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/client-oauth2/src 的OAuth模块。导入/依赖:外部:无；内部:无；本地:./client-oauth2、./constants。导出:expects、AuthError、getAuthError、auth、getRequestOptions。关键函数/方法:getAuthError、toString、auth、getRequestOptions。用于承载OAuth实现细节，并通过导出对外提供能力。注释目标:eslint-disable @typescript-eslint/no-explicit-any。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/client-oauth2 treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/client-oauth2/src/utils.ts -> services/n8n/infrastructure/n8n-client-oauth2/external_services/clients/utils.py

/* eslint-disable @typescript-eslint/no-explicit-any */
import type { ClientOAuth2Options, ClientOAuth2RequestObject } from './client-oauth2';
import { ERROR_RESPONSES } from './constants';

/**
 * Check if properties exist on an object and throw when they aren't.
 */
export function expects<Keys extends keyof ClientOAuth2Options>(
	obj: ClientOAuth2Options,
	...keys: Keys[]
): asserts obj is ClientOAuth2Options & {
	[K in Keys]: NonNullable<ClientOAuth2Options[K]>;
} {
	for (const key of keys) {
		if (obj[key] === null || obj[key] === undefined) {
			throw new TypeError('Expected "' + key + '" to exist');
		}
	}
}

export class AuthError extends Error {
	constructor(
		message: string,
		readonly body: any,
		readonly code = 'EAUTH',
	) {
		super(message);
	}
}

/**
 * Pull an authentication error from the response data.
 */
export function getAuthError(body: {
	error: string;
	error_description?: string;
}): Error | undefined {
	const message: string | undefined =
		ERROR_RESPONSES[body.error] ?? body.error_description ?? body.error;

	if (message) {
		return new AuthError(message, body);
	}

	return undefined;
}

/**
 * Ensure a value is a string.
 */
function toString(str: string | null | undefined) {
	return str === null ? '' : String(str);
}

/**
 * Create basic auth header.
 */
export function auth(username: string, password: string): string {
	return 'Basic ' + Buffer.from(toString(username) + ':' + toString(password)).toString('base64');
}

/**
 * Merge request options from an options object.
 */
export function getRequestOptions(
	{ url, method, body, query, headers }: ClientOAuth2RequestObject,
	options: ClientOAuth2Options,
): ClientOAuth2RequestObject {
	const rOptions = {
		url,
		method,
		body: { ...body, ...options.body },
		query: { ...query, ...options.query },
		headers: headers ?? {},
		ignoreSSLIssues: options.ignoreSSLIssues,
	};
	// if request authorization was overridden delete it from header
	if (rOptions.headers.Authorization === '') {
		delete rOptions.headers.Authorization;
	}
	return rOptions;
}
