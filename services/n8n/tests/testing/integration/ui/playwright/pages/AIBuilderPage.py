"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/AIBuilderPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:AIBuilderPage。关键函数/方法:getWorkflowSuggestions、getSuggestionPills、getCanvasBuildWithAIButton、waitForWorkflowBuildComplete。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/AIBuilderPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/AIBuilderPage.py

import type { Page } from '@playwright/test';

/**
 * Page object for AI Workflow Builder interactions
 */
export class AIBuilderPage {
	readonly page: Page;

	constructor(page: Page) {
		this.page = page;
	}

	// #region Locators

	getWorkflowSuggestions() {
		return this.page.getByTestId('workflow-suggestions');
	}

	getSuggestionPills() {
		// Get buttons within the pills container section, not the prompt input section
		return this.getWorkflowSuggestions()
			.locator('section[aria-label="Workflow suggestions"]')
			.getByRole('button');
	}

	getCanvasBuildWithAIButton() {
		return this.page.getByTestId('canvas-build-with-ai-button');
	}

	// #endregion

	// #region Actions

	async waitForWorkflowBuildComplete(options?: { timeout?: number }) {
		const timeout = options?.timeout ?? 300000; // Default 5 minutes
		const workingIndicator = this.page.getByText('Working...');

		// First wait for the indicator to appear (building has started)
		await workingIndicator.waitFor({ state: 'visible', timeout });

		// Then wait for it to disappear (building is complete)
		await workingIndicator.waitFor({ state: 'hidden', timeout });
	}

	// #endregion
}
