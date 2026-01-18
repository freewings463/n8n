"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/utils/http-proxy-agent.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/utils 的工作流工具。导入/依赖:外部:proxy-from-env、undici；内部:无；本地:无。导出:getProxyAgent。关键函数/方法:getProxyAgent。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected external HTTP client usage -> infrastructure/external_services/clients
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/utils/http-proxy-agent.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/external_services/clients/utils/http_proxy_agent.py

import proxyFromEnv from 'proxy-from-env';
import { ProxyAgent } from 'undici';

/**
 * Returns a ProxyAgent or undefined based on the environment variables and target URL.
 * When target URL is not provided, NO_PROXY environment variable is not respected.
 */
export function getProxyAgent(targetUrl?: string) {
	// There are cases where we don't know the target URL in advance (e.g. when we need to provide a proxy agent to ChatAwsBedrock)
	// In such case we use a dummy URL.
	// This will lead to `NO_PROXY` environment variable not being respected, but it is better than not having a proxy agent at all.
	const proxyUrl = proxyFromEnv.getProxyForUrl(targetUrl ?? 'https://example.nonexistent/');

	if (!proxyUrl) {
		return undefined;
	}

	return new ProxyAgent(proxyUrl);
}
