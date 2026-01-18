"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/WorkflowActivationModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的工作流页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:WorkflowActivationModal。关键函数/方法:getModal、getDontShowAgainCheckbox、getGotItButton、close、clickDontShowAgain、clickGotIt。用于组装工作流页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/WorkflowActivationModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/WorkflowActivationModal.py

import type { Locator } from '@playwright/test';

import { BasePage } from './BasePage';

export class WorkflowActivationModal extends BasePage {
	getModal(): Locator {
		return this.page.getByTestId('activation-modal');
	}

	getDontShowAgainCheckbox(): Locator {
		return this.getModal().getByText("Don't show again");
	}

	getGotItButton(): Locator {
		return this.getModal().getByRole('button', { name: 'Got it' });
	}

	async close(): Promise<void> {
		await this.getDontShowAgainCheckbox().click();

		await this.getGotItButton().click();
	}

	async clickDontShowAgain(): Promise<void> {
		await this.getDontShowAgainCheckbox().click();
	}

	async clickGotIt(): Promise<void> {
		await this.getGotItButton().click();
	}
}
