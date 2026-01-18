"""
MIGRATION-META:
  source_path: packages/@n8n/client-oauth2/src/client-oauth2-token.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/client-oauth2/src 的OAuth模块。导入/依赖:外部:node:assert；内部:无；本地:./client-oauth2、./constants、./utils。导出:ClientOAuth2TokenData、ClientOAuth2Token。关键函数/方法:sign、refresh、expired。用于承载OAuth实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/client-oauth2 treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/client-oauth2/src/client-oauth2-token.ts -> services/n8n/infrastructure/n8n-client-oauth2/external_services/clients/client_oauth2_token.py

import * as a from 'node:assert';

import type { ClientOAuth2, ClientOAuth2Options, ClientOAuth2RequestObject } from './client-oauth2';
import { DEFAULT_HEADERS } from './constants';
import { auth, getRequestOptions } from './utils';

export interface ClientOAuth2TokenData extends Record<string, string | undefined> {
	token_type?: string | undefined;
	access_token: string;
	refresh_token: string;
	expires_in?: string;
	scope?: string | undefined;
}

/**
 * General purpose client token generator.
 */
export class ClientOAuth2Token {
	readonly tokenType?: string;

	readonly accessToken: string;

	readonly refreshToken: string;

	private expires: Date;

	constructor(
		readonly client: ClientOAuth2,
		readonly data: ClientOAuth2TokenData,
	) {
		this.tokenType = data.token_type?.toLowerCase() ?? 'bearer';
		this.accessToken = data.access_token;
		this.refreshToken = data.refresh_token;

		this.expires = new Date();
		this.expires.setSeconds(this.expires.getSeconds() + Number(data.expires_in));
	}

	/**
	 * Sign a standardized request object with user authentication information.
	 */
	sign(requestObject: ClientOAuth2RequestObject): ClientOAuth2RequestObject {
		if (!this.accessToken) {
			throw new Error('Unable to sign without access token');
		}

		requestObject.headers = requestObject.headers ?? {};

		if (this.tokenType === 'bearer') {
			requestObject.headers.Authorization = 'Bearer ' + this.accessToken;
		} else {
			const parts = requestObject.url.split('#');
			const token = 'access_token=' + this.accessToken;
			const url = parts[0].replace(/[?&]access_token=[^&#]/, '');
			const fragment = parts[1] ? '#' + parts[1] : '';

			// Prepend the correct query string parameter to the url.
			requestObject.url = url + (url.indexOf('?') > -1 ? '&' : '?') + token + fragment;

			// Attempt to avoid storing the url in proxies, since the access token
			// is exposed in the query parameters.
			requestObject.headers.Pragma = 'no-store';
			requestObject.headers['Cache-Control'] = 'no-store';
		}

		return requestObject;
	}

	/**
	 * Refresh a user access token with the refresh token.
	 * As in RFC 6749 Section 6: https://www.rfc-editor.org/rfc/rfc6749.html#section-6
	 * Supports PKCE flows (RFC 7636) for public clients without client secret
	 */
	async refresh(opts?: ClientOAuth2Options): Promise<ClientOAuth2Token> {
		const options = { ...this.client.options, ...opts };

		a.ok(this.refreshToken, 'refreshToken is required');

		const { clientId, clientSecret } = options;
		const headers = { ...DEFAULT_HEADERS };
		const body: Record<string, string> = {
			refresh_token: this.refreshToken,
			grant_type: 'refresh_token',
		};

		// Handle different authentication methods
		if (clientSecret) {
			// Confidential client (traditional OAuth2 or PKCE with client secret)
			if (options.authentication === 'body') {
				body.client_id = clientId;
				body.client_secret = clientSecret;
			} else {
				headers.Authorization = auth(clientId, clientSecret);
			}
		} else {
			// Public client (PKCE without client secret per RFC 7636)
			// Always include client_id in body for public clients
			body.client_id = clientId;
		}

		const requestOptions = getRequestOptions(
			{
				url: options.accessTokenUri,
				method: 'POST',
				headers,
				body,
			},
			options,
		);

		const responseData = await this.client.accessTokenRequest(requestOptions);
		return this.client.createToken({ ...this.data, ...responseData });
	}

	/**
	 * Check whether the token has expired.
	 */
	expired(): boolean {
		return Date.now() > this.expires.getTime();
	}
}
