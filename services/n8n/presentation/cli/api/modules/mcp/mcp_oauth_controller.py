"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/mcp.oauth.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/mcp 的OAuth控制器。导入/依赖:外部:@modelcontextprotocol/sdk/…/authorize.js、@modelcontextprotocol/sdk/…/register.js、@modelcontextprotocol/sdk/…/revoke.js 等2项；内部:@n8n/decorators、@n8n/di、@/services/url.service；本地:./mcp-oauth-service。导出:McpOAuthController。关键函数/方法:setCorsHeaders、metadataOptions、metadata、ResourceMetadataOptions、ResourceMetadata。用于处理OAuth接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/mcp.oauth.controller.ts -> services/n8n/presentation/cli/api/modules/mcp/mcp_oauth_controller.py

import { authorizationHandler } from '@modelcontextprotocol/sdk/server/auth/handlers/authorize.js';
import { clientRegistrationHandler } from '@modelcontextprotocol/sdk/server/auth/handlers/register.js';
import { revocationHandler } from '@modelcontextprotocol/sdk/server/auth/handlers/revoke.js';
import { tokenHandler } from '@modelcontextprotocol/sdk/server/auth/handlers/token.js';
import { Get, Options, RootLevelController, StaticRouterMetadata } from '@n8n/decorators';
import { Container } from '@n8n/di';
import type { Response, Request, Router } from 'express';

import { UrlService } from '@/services/url.service';

import { McpOAuthService, SUPPORTED_SCOPES } from './mcp-oauth-service';

const mcpOAuthService = Container.get(McpOAuthService);

@RootLevelController('/')
export class McpOAuthController {
	constructor(private readonly urlService: UrlService) {}

	// Add CORS headers for OAuth discovery endpoints
	private setCorsHeaders(res: Response) {
		// Allow requests from any origin for OAuth discovery
		res.header('Access-Control-Allow-Origin', '*');
		res.header('Access-Control-Allow-Methods', 'GET, OPTIONS');
		res.header('Access-Control-Allow-Headers', 'Content-Type');
	}

	static routers: StaticRouterMetadata[] = [
		{
			path: '/mcp-oauth/register',
			router: clientRegistrationHandler({ clientsStore: mcpOAuthService.clientsStore }) as Router,
			skipAuth: true,
		},
		{
			path: '/mcp-oauth/authorize',
			router: authorizationHandler({ provider: mcpOAuthService }) as Router,
			skipAuth: true,
		},
		{
			path: '/mcp-oauth/token',
			router: tokenHandler({ provider: mcpOAuthService }) as Router,
			skipAuth: true,
		},
		{
			path: '/mcp-oauth/revoke',
			router: revocationHandler({ provider: mcpOAuthService }) as Router,
			skipAuth: true,
		},
	];

	@Options('/.well-known/oauth-authorization-server', { skipAuth: true, usesTemplates: true })
	metadataOptions(_req: Request, res: Response) {
		this.setCorsHeaders(res);
		res.status(204).end();
	}

	@Get('/.well-known/oauth-authorization-server', { skipAuth: true, usesTemplates: true })
	metadata(_req: Request, res: Response) {
		this.setCorsHeaders(res);

		const baseUrl = this.urlService.getInstanceBaseUrl();
		const metadata = {
			issuer: baseUrl,
			authorization_endpoint: `${baseUrl}/mcp-oauth/authorize`,
			token_endpoint: `${baseUrl}/mcp-oauth/token`,
			registration_endpoint: `${baseUrl}/mcp-oauth/register`,
			revocation_endpoint: `${baseUrl}/mcp-oauth/revoke`,
			response_types_supported: ['code'],
			grant_types_supported: ['authorization_code', 'refresh_token'],
			token_endpoint_auth_methods_supported: ['none', 'client_secret_post', 'client_secret_basic'],
			code_challenge_methods_supported: ['S256'],
			scopes_supported: SUPPORTED_SCOPES,
		};

		res.json(metadata);
	}

	@Options('/.well-known/oauth-protected-resource/mcp-server/http', {
		skipAuth: true,
		usesTemplates: true,
	})
	protectedResourceMetadataOptions(_req: Request, res: Response) {
		this.setCorsHeaders(res);
		res.status(204).end();
	}

	@Get('/.well-known/oauth-protected-resource/mcp-server/http', {
		skipAuth: true,
		usesTemplates: true,
	})
	protectedResourceMetadata(_req: Request, res: Response) {
		this.setCorsHeaders(res);

		const baseUrl = this.urlService.getInstanceBaseUrl();
		res.json({
			resource: `${baseUrl}/mcp-server/http`,
			bearer_methods_supported: ['header'],
			authorization_servers: [baseUrl],
			scopes_supported: SUPPORTED_SCOPES,
		});
	}
}
