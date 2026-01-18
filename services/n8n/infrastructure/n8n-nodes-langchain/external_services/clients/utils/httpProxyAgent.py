"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/httpProxyAgent.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils 的工具。导入/依赖:外部:https-proxy-agent、proxy-from-env、undici；内部:无；本地:无。导出:getProxyAgent、getNodeProxyAgent。关键函数/方法:getProxyUrlFromEnv、getProxyAgent、proxyFetch、getNodeProxyAgent。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected external HTTP client usage -> infrastructure/external_services/clients
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/httpProxyAgent.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/clients/utils/httpProxyAgent.py

import { HttpsProxyAgent } from 'https-proxy-agent';
import proxyFromEnv from 'proxy-from-env';
import { ProxyAgent } from 'undici';

/**
 * Resolves the proxy URL from environment variables for a given target URL.
 *
 * @param targetUrl - The target URL to check proxy configuration for (optional)
 * @returns The proxy URL string or undefined if no proxy is configured
 *
 * @remarks
 * There are cases where we don't know the target URL in advance (e.g. when we need to provide a proxy agent to ChatAwsBedrock).
 * In such case we use a dummy URL.
 * This will lead to `NO_PROXY` environment variable not being respected, but it is better than not having a proxy agent at all.
 */
function getProxyUrlFromEnv(targetUrl?: string): string {
	return proxyFromEnv.getProxyForUrl(targetUrl ?? 'https://example.nonexistent/');
}

/**
 * Returns a ProxyAgent or undefined based on the environment variables and target URL.
 * When target URL is not provided, NO_PROXY environment variable is not respected.
 */
export function getProxyAgent(targetUrl?: string) {
	const proxyUrl = getProxyUrlFromEnv(targetUrl);

	if (!proxyUrl) {
		return undefined;
	}

	return new ProxyAgent(proxyUrl);
}

/**
 * Make a fetch() request with a ProxyAgent if proxy environment variables are set.
 * If no proxy is configured, use the default fetch().
 */
export async function proxyFetch(input: string | URL, init?: RequestInit): Promise<Response> {
	return await fetch(input, {
		...init,
		// @ts-expect-error - dispatcher is an undici-specific option not in standard fetch
		dispatcher: getProxyAgent(input.toString()),
	});
}

/**
 * Returns a Node.js HTTP/HTTPS proxy agent for use with AWS SDK v3 clients.
 * AWS SDK v3 requires Node.js http.Agent/https.Agent instances (not undici ProxyAgent).
 *
 * @param targetUrl - The target URL to check proxy configuration for
 * @returns HttpsProxyAgent instance or undefined if no proxy is configured
 */
export function getNodeProxyAgent(targetUrl?: string) {
	const proxyUrl = getProxyUrlFromEnv(targetUrl);

	if (!proxyUrl) {
		return undefined;
	}

	return new HttpsProxyAgent(proxyUrl);
}
