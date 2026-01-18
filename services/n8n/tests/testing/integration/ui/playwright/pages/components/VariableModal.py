"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/VariableModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:VariableModal。关键函数/方法:save、getModal、getKeyInput、getValueInput、waitForModal、getSaveButton、close、addVariable。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/VariableModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/VariableModal.py

import type { Locator } from '@playwright/test';

/**
 * Variable modal component for canvas and variables interactions.
 * Used within VariablesPage as `n8n.variables.modal.*`
 *
 * @example
 * // Access via canvas page or variables page
 * await n8n.variables.modal.addVariable();
 * await expect(n8n.variables.modal.getModal()).toBeVisible();
 */
export class VariableModal {
	constructor(private root: Locator) {}

	getModal(): Locator {
		return this.root;
	}

	getKeyInput(): Locator {
		return this.root.getByTestId('variable-modal-key-input').getByRole('textbox');
	}

	getValueInput(): Locator {
		return this.root.getByTestId('variable-modal-value-input').getByRole('textbox');
	}

	async waitForModal(): Promise<void> {
		await this.root.waitFor({ state: 'visible' });
	}

	getSaveButton(): Locator {
		return this.root.getByTestId('variable-modal-save-button');
	}

	async save(): Promise<void> {
		const saveBtn = this.getSaveButton();
		await saveBtn.click();
	}

	async close(): Promise<void> {
		const closeBtn = this.root.locator('.el-dialog__close').first();
		if (await closeBtn.isVisible()) {
			await closeBtn.click();
		}
	}

	/**
	 * Add a variable to the modal
	 * @param key - The variable key
	 * @param value - The variable value
	 * @param options - The options to pass to the modal
	 * @param options.closeDialog - Whether to close the modal after saving
	 */
	async addVariable(
		key: string,
		value: string,
		{ shouldSave }: { shouldSave: boolean } = { shouldSave: true },
	): Promise<void> {
		await this.getKeyInput().fill(key);
		await this.getValueInput().fill(value);
		if (shouldSave) {
			console.log('Saving variable from modal');
			await this.save();
		}
	}
}
