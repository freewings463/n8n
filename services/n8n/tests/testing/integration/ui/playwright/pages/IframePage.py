"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/IframePage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:无；内部:无；本地:./BasePage。导出:IframePage。关键函数/方法:getIframe、getIframeBySrc、waitForIframeRequest。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/IframePage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/IframePage.py

import { BasePage } from './BasePage';

export class IframePage extends BasePage {
	getIframe() {
		return this.page.locator('iframe');
	}

	getIframeBySrc(src: string) {
		return this.page.locator(`iframe[src="${src}"]`);
	}

	async waitForIframeRequest(url: string) {
		await this.page.waitForResponse(url);
	}
}
