"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/mcp-oauth.helpers.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/mcp 的OAuth工具。导入/依赖:外部:无；内部:无；本地:无。导出:McpOAuthHelpers。关键函数/方法:buildSuccessRedirectUrl、buildErrorRedirectUrl。用于提供OAuth通用工具能力（纯函数/封装器）供复用。注释目标:Static utility functions for OAuth URL building。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/mcp-oauth.helpers.ts -> services/n8n/application/cli/services/modules/mcp/mcp_oauth_helpers.py

/**
 * Static utility functions for OAuth URL building
 */
export class McpOAuthHelpers {
	/**
	 * Build success redirect URL with authorization code
	 * Used when user approves consent
	 */
	static buildSuccessRedirectUrl(redirectUri: string, code: string, state: string | null): string {
		const targetUrl = new URL(redirectUri);
		targetUrl.searchParams.set('code', code);
		if (state) {
			targetUrl.searchParams.set('state', state);
		}
		return targetUrl.toString();
	}

	/**
	 * Build error redirect URL
	 * Used when user denies consent or errors occur
	 */
	static buildErrorRedirectUrl(
		redirectUri: string,
		error: string,
		errorDescription: string,
		state: string | null,
	): string {
		const targetUrl = new URL(redirectUri);
		targetUrl.searchParams.set('error', error);
		targetUrl.searchParams.set('error_description', errorDescription);
		if (state) {
			targetUrl.searchParams.set('state', state);
		}
		return targetUrl.toString();
	}
}
