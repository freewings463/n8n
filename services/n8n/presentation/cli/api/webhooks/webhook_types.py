"""
MIGRATION-META:
  source_path: packages/cli/src/webhooks/webhook.types.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/webhooks 的Webhook类型。导入/依赖:外部:express；内部:n8n-workflow；本地:无。导出:WebhookOptionsRequest、WebhookRequest、WaitingWebhookRequest、WebhookAccessControlOptions、IWebhookManager、IWebhookResponseCallbackData、Method、WebhookResponseHeaders 等1项。关键函数/方法:executeWebhook。用于定义Webhook相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/webhooks/webhook.types.ts -> services/n8n/presentation/cli/api/webhooks/webhook_types.py

import type { Request, Response } from 'express';
import type { IDataObject, IHttpRequestMethods } from 'n8n-workflow';

export type WebhookOptionsRequest = Request & { method: 'OPTIONS' };

export type WebhookRequest = Request<{ path: string }> & {
	method: IHttpRequestMethods;
	params: Record<string, string>;
};

export type WaitingWebhookRequest = WebhookRequest & {
	params: Pick<WebhookRequest['params'], 'path'> & { suffix?: string };
};

export interface WebhookAccessControlOptions {
	allowedOrigins?: string;
}

export interface IWebhookManager {
	/** Gets all request methods associated with a webhook path*/
	getWebhookMethods?: (path: string) => Promise<IHttpRequestMethods[]>;

	/** Find the CORS options matching a path and method */
	findAccessControlOptions?: (
		path: string,
		httpMethod: IHttpRequestMethods,
	) => Promise<WebhookAccessControlOptions | undefined>;

	executeWebhook(req: WebhookRequest, res: Response): Promise<IWebhookResponseCallbackData>;
}

export interface IWebhookResponseCallbackData {
	data?: IDataObject | IDataObject[];
	headers?: object;
	noWebhookResponse?: boolean;
	responseCode?: number;
}

export type Method = NonNullable<IHttpRequestMethods>;

/** Response headers. Keys are always lower-cased. */
export type WebhookResponseHeaders = Map<string, string>;

/**
 * The headers object that node's `responseHeaders` property can return
 */
export type WebhookNodeResponseHeaders = {
	entries?: Array<{
		name: string;
		value: string;
	}>;
};
