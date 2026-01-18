"""
MIGRATION-META:
  source_path: packages/testing/playwright/utils/url-helper.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:getPortFromUrl、getBackendUrl、getFrontendUrl。关键函数/方法:getPortFromUrl、getBackendUrl、getFrontendUrl。用于提供该模块通用工具能力（纯函数/封装器）供复用。注释目标:Extract port from a URL string。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/utils/url-helper.ts -> services/n8n/tests/testing/integration/ui/playwright/utils/url_helper.py

/**
 * Extract port from a URL string
 */
export function getPortFromUrl(url: string): string {
	const parsedUrl = new URL(url);
	return parsedUrl.port || (parsedUrl.protocol === 'https:' ? '443' : '80');
}

/**
 * Get the backend URL from environment variables
 * Returns N8N_BASE_URL
 */
export function getBackendUrl(): string | undefined {
	return process.env.N8N_BASE_URL;
}

/**
 * Get the frontend URL from environment variables
 * When N8N_EDITOR_URL is set (dev mode), use it for the frontend
 * Otherwise, use the same URL as the backend
 */
export function getFrontendUrl(): string | undefined {
	return process.env.N8N_EDITOR_URL ?? process.env.N8N_BASE_URL;
}
