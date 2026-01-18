"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/WorkflowCredentialSetupModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的工作流页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:WorkflowCredentialSetupModal。关键函数/方法:getModal、getContinueButton、clickContinue。用于组装工作流页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/WorkflowCredentialSetupModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/WorkflowCredentialSetupModal.py

import type { Locator } from '@playwright/test';

import { BasePage } from './BasePage';

/**
 * Page object for the Workflow Credential Setup Modal
 * This modal appears in the workflow editor when users need to complete credential setup
 * after skipping or partially completing it during template setup
 */
export class WorkflowCredentialSetupModal extends BasePage {
	/**
	 * Get the workflow credential setup modal
	 * @returns Locator for the modal element
	 */
	getModal(): Locator {
		return this.page.getByTestId('setup-workflow-credentials-modal');
	}

	/**
	 * Get the continue button in the modal
	 * @returns Locator for the continue button
	 */
	getContinueButton(): Locator {
		return this.page.getByTestId('continue-button');
	}

	/**
	 * Click the continue button to close the modal
	 */
	async clickContinue(): Promise<void> {
		await this.getContinueButton().click();
	}
}
