"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/mcp.module.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/mcp 的模块。导入/依赖:外部:无；内部:@n8n/decorators、@n8n/di；本地:./mcp.controller、./mcp.settings.controller、./mcp.oauth.controller、./mcp.auth.consent.controller 等7项。导出:McpModule。关键函数/方法:init、settings、entities、shutdown。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/mcp.module.ts -> services/n8n/application/cli/services/modules/mcp/mcp_module.py

import type { ModuleInterface } from '@n8n/decorators';
import { BackendModule, OnShutdown } from '@n8n/decorators';
import { Container } from '@n8n/di';

/**
 * Handles instance-level MCP access.
 * Runs MCP server and exposes endpoints for MCP clients to connect to.
 * Requires MCP access to be enabled in settings and a valid API key.
 */
@BackendModule({ name: 'mcp' })
export class McpModule implements ModuleInterface {
	async init() {
		await import('./mcp.controller');
		await import('./mcp.settings.controller');
		await import('./mcp.oauth.controller');
		await import('./mcp.auth.consent.controller');
		await import('./mcp.oauth-clients.controller');

		// Initialize event relay to handle workflow deactivation
		const { McpEventRelay } = await import('./mcp.event-relay');
		Container.get(McpEventRelay).init();
	}

	/**
	 * Settings exposed to the frontend under `/rest/module-settings`.
	 *
	 * The response shape will be `{ mcp: { mcpAccessEnabled: boolean } }`.
	 */
	async settings() {
		const { McpSettingsService } = await import('./mcp.settings.service');
		const mcpAccessEnabled = await Container.get(McpSettingsService).getEnabled();
		return { mcpAccessEnabled };
	}

	async entities() {
		const { OAuthClient } = await import('./database/entities/oauth-client.entity');
		const { AuthorizationCode } = await import(
			'./database/entities/oauth-authorization-code.entity'
		);
		const { AccessToken } = await import('./database/entities/oauth-access-token.entity');
		const { RefreshToken } = await import('./database/entities/oauth-refresh-token.entity');
		const { UserConsent } = await import('./database/entities/oauth-user-consent.entity');

		return [OAuthClient, AuthorizationCode, AccessToken, RefreshToken, UserConsent] as never;
	}

	@OnShutdown()
	async shutdown() {}
}
