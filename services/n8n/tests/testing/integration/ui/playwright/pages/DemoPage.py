"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/DemoPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:无；内部:无；本地:./BasePage。导出:DemoPage。关键函数/方法:visitDemoPage、importWorkflow、getBody。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/DemoPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/DemoPage.py

import { BasePage } from './BasePage';

export class DemoPage extends BasePage {
	async visitDemoPage(theme?: 'dark' | 'light') {
		const query = theme ? `?theme=${theme}` : '';
		await this.page.goto('/workflows/demo' + query);
		await this.getBody().waitFor({ state: 'visible' });
		await this.page.evaluate(() => {
			// @ts-expect-error - this is a custom property added by the demo page
			window.preventNodeViewBeforeUnload = true;
		});
	}

	/**
	 * Import a workflow into the demo page
	 * @param workflow - The workflow to import
	 */
	async importWorkflow(workflow: object) {
		const OPEN_WORKFLOW = { command: 'openWorkflow', workflow };
		await this.page.evaluate((message) => {
			console.log('Posting message:', JSON.stringify(message));
			window.postMessage(JSON.stringify(message), '*');
		}, OPEN_WORKFLOW);
	}

	getBody() {
		return this.page.locator('body');
	}
}
