"""
MIGRATION-META:
  source_path: packages/core/src/html-sandbox.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src 的模块。导入/依赖:外部:无；内部:@n8n/config、@n8n/di；本地:无。导出:isWebhookHtmlSandboxingDisabled、getWebhookSandboxCSP、isHtmlRenderedContentType。关键函数/方法:isWebhookHtmlSandboxingDisabled、getWebhookSandboxCSP、isHtmlRenderedContentType。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core src/* defaulted to execution engine application services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/html-sandbox.ts -> services/n8n/application/core/services/execution_engine/html_sandbox.py

import { SecurityConfig } from '@n8n/config';
import { Container } from '@n8n/di';

export const isWebhookHtmlSandboxingDisabled = () => {
	return Container.get(SecurityConfig).disableWebhookHtmlSandboxing;
};

/**
 * Returns the CSP header value that sandboxes the HTML page into a separate origin.
 */
export const getWebhookSandboxCSP = (): string => {
	return 'sandbox allow-downloads allow-forms allow-modals allow-orientation-lock allow-pointer-lock allow-popups allow-presentation allow-scripts allow-top-navigation allow-top-navigation-by-user-activation allow-top-navigation-to-custom-protocols';
};

/**
 * Checks if the given content type is something a browser might render
 * as HTML.
 */
export const isHtmlRenderedContentType = (contentType: string) => {
	const contentTypeLower = contentType.trim().toLowerCase();

	return (
		// The content-type can also contain a charset, e.g. "text/html; charset=utf-8"
		contentTypeLower.startsWith('text/html') || contentTypeLower.startsWith('application/xhtml+xml')
	);
};
