"""
MIGRATION-META:
  source_path: packages/@n8n/client-oauth2/src/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/client-oauth2/src 的OAuth类型。导入/依赖:外部:无；内部:无；本地:无。导出:Headers、OAuth2GrantType、OAuth2AuthenticationMethod、OAuth2CredentialData、OAuth2AccessTokenErrorResponse。关键函数/方法:无。用于定义OAuth相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/client-oauth2 treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/client-oauth2/src/types.ts -> services/n8n/infrastructure/n8n-client-oauth2/external_services/clients/types.py

export type Headers = Record<string, string | string[]>;

export type OAuth2GrantType = 'pkce' | 'authorizationCode' | 'clientCredentials';

export type OAuth2AuthenticationMethod = 'header' | 'body';

export interface OAuth2CredentialData {
	clientId: string;
	clientSecret?: string;
	accessTokenUrl: string;
	authentication?: OAuth2AuthenticationMethod;
	authUrl?: string;
	scope?: string;
	authQueryParameters?: string;
	additionalBodyProperties?: string;
	grantType: OAuth2GrantType;
	ignoreSSLIssues?: boolean;
	oauthTokenData?: {
		access_token: string;
		refresh_token?: string;
	};
	useDynamicClientRegistration?: boolean;
	serverUrl?: string;
}

/**
 * The response from the OAuth2 server when the access token is not successfully
 * retrieved. As specified in RFC 6749 Section 5.2:
 * https://www.rfc-editor.org/rfc/rfc6749.html#section-5.2
 */
export interface OAuth2AccessTokenErrorResponse extends Record<string, unknown> {
	error: string;
	error_description?: string;
	error_uri?: string;
}
