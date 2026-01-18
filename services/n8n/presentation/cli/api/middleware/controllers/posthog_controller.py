"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/posthog.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的控制器。导入/依赖:外部:express、http-proxy-middleware；内部:@n8n/config、@n8n/db、@n8n/decorators；本地:无。导出:PostHogController。关键函数/方法:fixRequestBody、capture、decide、sessionRecording、sessionEvents、engage、batch、flags、staticArrayJs、staticLazyRecorderJs 等1项。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/posthog.controller.ts -> services/n8n/presentation/cli/api/middleware/controllers/posthog_controller.py

import { GlobalConfig } from '@n8n/config';
import { AuthenticatedRequest } from '@n8n/db';
import { Get, Post, RestController } from '@n8n/decorators';
import { NextFunction, Response } from 'express';
import { createProxyMiddleware, fixRequestBody } from 'http-proxy-middleware';

@RestController('/posthog')
export class PostHogController {
	proxy;

	constructor(private readonly globalConfig: GlobalConfig) {
		const targetUrl = this.globalConfig.diagnostics.posthogConfig.apiHost;

		this.proxy = createProxyMiddleware({
			target: targetUrl,
			changeOrigin: true,

			pathRewrite: {
				'^/posthog/': '/',
			},
			on: {
				proxyReq: (proxyReq, req) => {
					proxyReq.removeHeader('cookie');

					if (req.method === 'POST') {
						fixRequestBody(proxyReq, req);
					}
				},
			},
		});
	}

	// Main event capture endpoint
	@Post('/capture/', { skipAuth: true, rateLimit: { limit: 200, windowMs: 60_000 } })
	async capture(req: AuthenticatedRequest, res: Response, next: NextFunction) {
		return await this.proxy(req, res, next);
	}

	// Feature flags and configuration
	@Post('/decide/', { skipAuth: true, rateLimit: { limit: 100, windowMs: 60_000 } })
	async decide(req: AuthenticatedRequest, res: Response, next: NextFunction) {
		return await this.proxy(req, res, next);
	}

	// Session recording events
	@Post('/s/', { skipAuth: true, rateLimit: { limit: 50, windowMs: 60_000 } })
	async sessionRecording(req: AuthenticatedRequest, res: Response, next: NextFunction) {
		return await this.proxy(req, res, next);
	}

	// Session recording events (alternative endpoint)
	@Post('/e/', { skipAuth: true, rateLimit: { limit: 50, windowMs: 60_000 } })
	async sessionEvents(req: AuthenticatedRequest, res: Response, next: NextFunction) {
		return await this.proxy(req, res, next);
	}

	// Person/profile updates
	@Post('/engage/', { skipAuth: true, rateLimit: { limit: 50, windowMs: 60_000 } })
	async engage(req: AuthenticatedRequest, res: Response, next: NextFunction) {
		return await this.proxy(req, res, next);
	}

	// Batch endpoint (for multiple events)
	@Post('/batch/', { skipAuth: true, rateLimit: { limit: 100, windowMs: 60_000 } })
	async batch(req: AuthenticatedRequest, res: Response, next: NextFunction) {
		return await this.proxy(req, res, next);
	}

	// Feature flags endpoint - /flags/
	@Post('/flags/', { skipAuth: true, rateLimit: { limit: 100, windowMs: 60_000 } })
	async flags(req: AuthenticatedRequest, res: Response, next: NextFunction) {
		return await this.proxy(req, res, next);
	}

	// Static files - specific endpoint for array.js and lazy-recorder.js
	@Get('/static/array.js', {
		skipAuth: true,
		usesTemplates: true,
		rateLimit: { limit: 50, windowMs: 60_000 },
	})
	staticArrayJs(req: AuthenticatedRequest, res: Response, next: NextFunction) {
		void this.proxy(req, res, next);
	}

	@Get('/static/lazy-recorder.js', {
		skipAuth: true,
		usesTemplates: true,
		rateLimit: { limit: 50, windowMs: 60_000 },
	})
	staticLazyRecorderJs(req: AuthenticatedRequest, res: Response, next: NextFunction) {
		void this.proxy(req, res, next);
	}

	// Configuration endpoints for array.js
	@Get('/array/:apiKey/config.js', {
		skipAuth: true,
		rateLimit: { limit: 20, windowMs: 60_000 },
		usesTemplates: true,
	})
	arrayConfig(req: AuthenticatedRequest, res: Response, next: NextFunction) {
		void this.proxy(req, res, next);
	}
}
