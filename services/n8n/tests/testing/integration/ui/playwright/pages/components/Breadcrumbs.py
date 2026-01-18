"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/Breadcrumbs.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:Breadcrumbs。关键函数/方法:getBreadcrumbs、getBreadcrumb、getCurrentBreadcrumb、getHiddenBreadcrumbs、getHomeProjectBreadcrumb、getHiddenBreadcrumb、getActionToggleDropdown、getFolderBreadcrumbsActionToggle、renameCurrentBreadcrumb。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/Breadcrumbs.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/Breadcrumbs.py

import type { Page } from '@playwright/test';

export class Breadcrumbs {
	constructor(private readonly page: Page) {}

	getBreadcrumbs() {
		return this.page.getByTestId('breadcrumbs-item');
	}

	getBreadcrumb(resourceName: string) {
		return this.getBreadcrumbs().filter({ hasText: resourceName });
	}
	getCurrentBreadcrumb() {
		return this.page.getByTestId('breadcrumbs-item-current');
	}

	getHiddenBreadcrumbs() {
		return this.page.getByTestId('hidden-items-menu');
	}

	getHomeProjectBreadcrumb() {
		return this.page.getByTestId('home-project');
	}

	getHiddenBreadcrumb(resourceName: string) {
		return this.getHiddenBreadcrumbs().filter({ hasText: resourceName });
	}

	getActionToggleDropdown(resourceName: string) {
		return this.page.getByTestId('action-toggle-dropdown').getByTestId(`action-${resourceName}`);
	}

	getFolderBreadcrumbsActionToggle() {
		return this.page.getByTestId('folder-breadcrumbs-actions');
	}

	/**
	 * Rename the current breadcrumb by activating inline edit mode
	 * @param newName - The new name for the breadcrumb item
	 */
	async renameCurrentBreadcrumb(newName: string) {
		await this.getCurrentBreadcrumb().getByTestId('inline-edit-preview').click();
		await this.getCurrentBreadcrumb().getByTestId('inline-edit-input').fill(newName);
		await this.page.keyboard.press('Enter');
	}
}