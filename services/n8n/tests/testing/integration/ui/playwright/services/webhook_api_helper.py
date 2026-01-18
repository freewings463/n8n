"""
MIGRATION-META:
  source_path: packages/testing/playwright/services/webhook-api-helper.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/services 的Webhook服务。导入/依赖:外部:@playwright/test；内部:无；本地:./api-helper。导出:WebhookApiHelper。关键函数/方法:trigger。用于封装Webhook业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/services/webhook-api-helper.ts -> services/n8n/tests/testing/integration/ui/playwright/services/webhook_api_helper.py

import type { APIResponse } from '@playwright/test';

import type { ApiHelpers } from './api-helper';

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH' | 'HEAD';

interface TriggerOptions {
	method?: HttpMethod;
	headers?: Record<string, string>;
	data?: unknown;
	/** Max retries for 404 (webhook not yet registered). Default: 3 */
	maxNotFoundRetries?: number;
	/** Delay between 404 retries in ms. Default: 250 */
	notFoundRetryDelayMs?: number;
}

/** Triggers webhooks with retry for 404s (async registration) and connection errors. */
export class WebhookApiHelper {
	constructor(private readonly api: ApiHelpers) {}

	async trigger(path: string, options?: TriggerOptions): Promise<APIResponse> {
		const maxNotFoundRetries = options?.maxNotFoundRetries ?? 3;
		const notFoundRetryDelayMs = options?.notFoundRetryDelayMs ?? 250;

		let lastResponse: APIResponse | undefined;

		for (let attempt = 0; attempt <= maxNotFoundRetries; attempt++) {
			lastResponse = await this.api.request.fetch(path, {
				method: options?.method ?? 'GET',
				headers: options?.headers,
				data: options?.data,
				maxRetries: 3, // Playwright retry for connection errors
			});

			if (lastResponse.status() !== 404 || attempt === maxNotFoundRetries) {
				return lastResponse;
			}

			await new Promise((resolve) => setTimeout(resolve, notFoundRetryDelayMs));
		}

		return lastResponse!;
	}
}
