"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/VersionsPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:无；内部:无；本地:./BasePage。导出:VersionsPage。关键函数/方法:getVersionUpdatesPanelOpenButton、getVersionUpdatesPanel、getVersionUpdatesPanelCloseButton、getVersionCard、getWhatsNewMenuItem、openWhatsNewMenu、openVersionUpdatesPanel、closeVersionUpdatesPanel。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/VersionsPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/VersionsPage.py

import { BasePage } from './BasePage';

export class VersionsPage extends BasePage {
	getVersionUpdatesPanelOpenButton() {
		return this.page.getByTestId('version-update-next-versions-link');
	}

	getVersionUpdatesPanel() {
		return this.page.getByTestId('version-updates-panel');
	}

	getVersionUpdatesPanelCloseButton() {
		return this.getVersionUpdatesPanel().getByRole('button', { name: 'Close' });
	}

	getVersionCard() {
		return this.page.getByTestId('version-card');
	}

	getWhatsNewMenuItem() {
		return this.page.getByTestId('whats-new');
	}

	async openWhatsNewMenu() {
		await this.getWhatsNewMenuItem().click();
	}

	async openVersionUpdatesPanel() {
		await this.getVersionUpdatesPanelOpenButton().click();
	}

	async closeVersionUpdatesPanel() {
		await this.getVersionUpdatesPanelCloseButton().click();
	}
}
