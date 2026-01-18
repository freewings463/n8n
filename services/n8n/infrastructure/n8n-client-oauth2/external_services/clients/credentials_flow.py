"""
MIGRATION-META:
  source_path: packages/@n8n/client-oauth2/src/credentials-flow.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/client-oauth2/src 的OAuth模块。导入/依赖:外部:无；内部:无；本地:./client-oauth2、./client-oauth2-token、./constants、./types 等1项。导出:CredentialsFlow。关键函数/方法:getToken、expects。用于承载OAuth实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/client-oauth2 treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/client-oauth2/src/credentials-flow.ts -> services/n8n/infrastructure/n8n-client-oauth2/external_services/clients/credentials_flow.py

import type { ClientOAuth2 } from './client-oauth2';
import type { ClientOAuth2Token } from './client-oauth2-token';
import { DEFAULT_HEADERS } from './constants';
import type { Headers } from './types';
import { auth, expects, getRequestOptions } from './utils';

interface CredentialsFlowBody {
	client_id?: string;
	client_secret?: string;
	grant_type: 'client_credentials';
	scope?: string;
}

/**
 * Support client credentials OAuth 2.0 grant.
 *
 * Reference: http://tools.ietf.org/html/rfc6749#section-4.4
 */
export class CredentialsFlow {
	constructor(private client: ClientOAuth2) {}

	/**
	 * Request an access token using the client credentials.
	 */
	async getToken(): Promise<ClientOAuth2Token> {
		const options = { ...this.client.options };
		expects(options, 'clientId', 'clientSecret', 'accessTokenUri');

		const headers: Headers = { ...DEFAULT_HEADERS };
		const body: CredentialsFlowBody = {
			grant_type: 'client_credentials',
			...(options.additionalBodyProperties ?? {}),
		};

		if (options.scopes !== undefined) {
			body.scope = options.scopes.join(options.scopesSeparator ?? ' ');
		}

		const clientId = options.clientId;
		const clientSecret = options.clientSecret;

		if (options.authentication === 'body') {
			body.client_id = clientId;
			body.client_secret = clientSecret;
		} else {
			headers.Authorization = auth(clientId, clientSecret);
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
		return this.client.createToken(responseData);
	}
}
