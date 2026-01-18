"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/TemplatesPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:TemplatesPage。关键函数/方法:getTemplateCards、getFirstTemplateCard、getUseTemplateButton、getTemplatesLoadingContainer、getDescription、getSearchInput、getAllCategoriesFilter、getCategoryFilters、clickFirstTemplateCard、getCategoryFilter 等6项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/TemplatesPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/TemplatesPage.py

import type { Locator } from '@playwright/test';

import { BasePage } from './BasePage';

export class TemplatesPage extends BasePage {
	getTemplateCards(): Locator {
		return this.page.getByTestId('template-card');
	}

	getFirstTemplateCard(): Locator {
		return this.getTemplateCards().first();
	}

	getUseTemplateButton(): Locator {
		return this.page.getByTestId('use-template-button');
	}

	getTemplatesLoadingContainer(): Locator {
		return this.page.getByTestId('templates-loading-container');
	}

	getDescription(): Locator {
		return this.page.getByTestId('template-description');
	}

	getSearchInput(): Locator {
		return this.page.getByTestId('template-search-input');
	}

	getAllCategoriesFilter(): Locator {
		return this.page.getByTestId('template-filter-all-categories');
	}

	getCategoryFilters(): Locator {
		return this.page.locator('[data-test-id^=template-filter]');
	}

	async clickFirstTemplateCard(): Promise<void> {
		await this.getFirstTemplateCard().click();
	}

	getCategoryFilter(category: string): Locator {
		return this.page.getByTestId(`template-filter-${category}`);
	}

	getTemplateCountLabel(): Locator {
		return this.page.getByTestId('template-count-label');
	}

	getCollectionCountLabel(): Locator {
		return this.page.getByTestId('collection-count-label');
	}

	getSkeletonLoader(): Locator {
		return this.page.locator('.el-skeleton.n8n-loading');
	}

	async clickUseTemplateButton(): Promise<void> {
		await this.getUseTemplateButton().click();
	}

	async clickCategoryFilter(category: string): Promise<void> {
		await this.getCategoryFilter(category).click();
	}

	/**
	 * Click the "Use workflow" button on a specific template card by workflow title
	 * @param workflowTitle - The title of the workflow to find on the template card
	 */
	async clickUseWorkflowButton(workflowTitle: string): Promise<void> {
		const templateCard = this.page.getByTestId('template-card').filter({ hasText: workflowTitle });
		await templateCard.hover();
		await templateCard.getByTestId('use-workflow-button').click();
	}
}
