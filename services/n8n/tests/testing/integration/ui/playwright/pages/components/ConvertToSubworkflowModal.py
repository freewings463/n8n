"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/ConvertToSubworkflowModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的工作流组件。导入/依赖:外部:@playwright/test；内部:无；本地:../BasePage。导出:ConvertToSubworkflowModal。关键函数/方法:getModal、getSubmitButton、waitForModal、clickSubmitButton、waitForClose。用于渲染工作流UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/ConvertToSubworkflowModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/ConvertToSubworkflowModal.py

import type { Locator } from '@playwright/test';

import { BasePage } from '../BasePage';

/**
 * Convert to Sub-workflow Modal component for converting nodes to sub-workflows.
 * Used within CanvasPage as `n8n.canvas.convertToSubworkflowModal.*`
 *
 * @example
 * // Access via canvas page
 * await n8n.canvas.rightClickNode('My Node');
 * await n8n.canvas.clickContextMenuAction('Convert node to sub-workflow');
 * await n8n.canvas.convertToSubworkflowModal.waitForModal();
 * await n8n.canvas.convertToSubworkflowModal.clickSubmitButton();
 * await n8n.canvas.convertToSubworkflowModal.waitForClose();
 */
export class ConvertToSubworkflowModal extends BasePage {
	constructor(private root: Locator) {
		super(root.page());
	}

	getModal(): Locator {
		return this.root;
	}

	getSubmitButton(): Locator {
		return this.root.getByTestId('submit-button');
	}

	async waitForModal(): Promise<void> {
		await this.root.waitFor({ state: 'visible' });
	}

	async clickSubmitButton(): Promise<void> {
		await this.getSubmitButton().click();
	}

	async waitForClose(): Promise<void> {
		await this.root.waitFor({ state: 'hidden' });
	}
}
