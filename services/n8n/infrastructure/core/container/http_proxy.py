"""
MIGRATION-META:
  source_path: packages/core/src/http-proxy.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src 的模块。导入/依赖:外部:http-proxy-agent、https-proxy-agent、proxy-from-env；内部:n8n-workflow；本地:无。导出:createHttpProxyAgent、createHttpsProxyAgent、installGlobalProxyAgent、uninstallGlobalProxyAgent。关键函数/方法:buildTargetUrl、extractHostInfo、addRequest、createHttpProxyAgent、createHttpsProxyAgent、hasProxyEnvironmentVariables、installGlobalProxyAgent、uninstallGlobalProxyAgent。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/http-proxy.ts -> services/n8n/infrastructure/core/container/http_proxy.py

import http from 'http';
import { HttpProxyAgent } from 'http-proxy-agent';
import https from 'https';
import { HttpsProxyAgent } from 'https-proxy-agent';
import { LoggerProxy } from 'n8n-workflow';
import proxyFromEnv from 'proxy-from-env';

type ProxyRequestParameters = Parameters<HttpProxyAgent<string>['addRequest']>;
type ProxyClientRequest = ProxyRequestParameters[0];
type ProxyRequestOptions = ProxyRequestParameters[1];

function buildTargetUrl(hostname: string, port: number, protocol: 'http' | 'https'): string {
	const defaultPort = protocol === 'https' ? 443 : 80;
	const portSuffix = port === defaultPort ? '' : `:${port}`;
	return `${protocol}://${hostname}${portSuffix}`;
}

function extractHostInfo(
	options: http.RequestOptions,
	defaultPort: number,
): { hostname: string; port: number } {
	const hostname = options.hostname ?? options.host ?? 'localhost';
	const port =
		typeof options.port === 'string' ? parseInt(options.port, 10) : (options.port ?? defaultPort);
	return { hostname: String(hostname), port: Number(port) };
}

function getOrCreateProxyAgent<T extends HttpProxyAgent<string> | HttpsProxyAgent<string>>(
	cache: Map<string, T>,
	proxyUrl: string,
	createAgent: (url: string) => T,
): T {
	let proxyAgent = cache.get(proxyUrl);
	if (!proxyAgent) {
		proxyAgent = createAgent(proxyUrl);
		cache.set(proxyUrl, proxyAgent);
	}
	return proxyAgent;
}

function createFallbackAgent<T extends http.Agent | https.Agent>(agentClass: new () => T): T {
	return new agentClass();
}

/**
 * Node.js is working on native HTTP proxy support (as of Node.js 24)
 * When it is stable we can use it and remove this implementation
 *
 * https://nodejs.org/api/http.html#built-in-proxy-support
 */
class HttpProxyManager extends http.Agent {
	private readonly proxyAgentCache = new Map<string, HttpProxyAgent<string>>();
	private readonly fallbackAgent = createFallbackAgent(http.Agent);

	addRequest(req: http.ClientRequest, options: http.RequestOptions) {
		const { hostname, port } = extractHostInfo(options, 80);
		const targetUrl = buildTargetUrl(hostname, port, 'http');
		const proxyUrl = proxyFromEnv.getProxyForUrl(targetUrl);

		if (proxyUrl) {
			const proxyAgent = getOrCreateProxyAgent(
				this.proxyAgentCache,
				proxyUrl,
				(url) => new HttpProxyAgent(url),
			);
			return proxyAgent.addRequest(req as ProxyClientRequest, options as ProxyRequestOptions);
		}

		return this.fallbackAgent.addRequest(req, options);
	}
}

class HttpsProxyManager extends https.Agent {
	private readonly proxyAgentCache = new Map<string, HttpsProxyAgent<string>>();
	private readonly fallbackAgent = createFallbackAgent(https.Agent);

	addRequest(req: http.ClientRequest, options: https.RequestOptions) {
		const { hostname, port } = extractHostInfo(options, 443);
		const targetUrl = buildTargetUrl(hostname, port, 'https');
		const proxyUrl = proxyFromEnv.getProxyForUrl(targetUrl);

		if (proxyUrl) {
			const proxyAgent = getOrCreateProxyAgent(
				this.proxyAgentCache,
				proxyUrl,
				(url) => new HttpsProxyAgent(url),
			);
			return proxyAgent.addRequest(req, options);
		}

		return this.fallbackAgent.addRequest(req, options);
	}
}

export function createHttpProxyAgent(
	customProxyUrl: string | null = null,
	targetUrl: string,
	options?: http.AgentOptions,
): http.Agent {
	const proxyUrl = customProxyUrl ?? proxyFromEnv.getProxyForUrl(targetUrl);

	if (proxyUrl) {
		return new HttpProxyAgent(proxyUrl, options);
	}

	return new http.Agent(options);
}

export function createHttpsProxyAgent(
	customProxyUrl: string | null = null,
	targetUrl: string,
	options?: https.AgentOptions,
): https.Agent {
	const proxyUrl = customProxyUrl ?? proxyFromEnv.getProxyForUrl(targetUrl);

	if (proxyUrl) {
		return new HttpsProxyAgent(proxyUrl, options);
	}

	return new https.Agent(options);
}

function hasProxyEnvironmentVariables(): boolean {
	return Boolean(
		process.env.HTTP_PROXY ??
			process.env.http_proxy ??
			process.env.HTTPS_PROXY ??
			process.env.https_proxy ??
			process.env.ALL_PROXY ??
			process.env.all_proxy,
	);
}

export function installGlobalProxyAgent(): void {
	if (hasProxyEnvironmentVariables()) {
		LoggerProxy.debug('Installing global HTTP proxy agents', {
			HTTP_PROXY: process.env.HTTP_PROXY ?? process.env.http_proxy,
			HTTPS_PROXY: process.env.HTTPS_PROXY ?? process.env.https_proxy,
			NO_PROXY: process.env.NO_PROXY ?? process.env.no_proxy,
			ALL_PROXY: process.env.ALL_PROXY ?? process.env.all_proxy,
		});

		http.globalAgent = new HttpProxyManager();
		https.globalAgent = new HttpsProxyManager();
	}
}

export function uninstallGlobalProxyAgent(): void {
	http.globalAgent = new http.Agent();
	https.globalAgent = new https.Agent();
}
