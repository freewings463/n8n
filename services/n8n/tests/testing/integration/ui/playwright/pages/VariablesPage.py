"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/VariablesPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage、./components/VariableModal。导出:VariablesPage。关键函数/方法:getUnavailableResourcesList、getResourcesList、getEmptyResourcesList、getEmptyResourcesListNewVariableButton、getSearchBar、getCreateVariableButton、getVariablesRows、getVariableRow、getEditableRowCancelButton、getEditableRowSaveButton 等5项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/VariablesPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/VariablesPage.py

import { expect, type Locator } from '@playwright/test';

import { BasePage } from './BasePage';
import { VariableModal } from './components/VariableModal';

export class VariablesPage extends BasePage {
	readonly variableModal = new VariableModal(this.page.getByTestId('variableModal-modal'));

	getUnavailableResourcesList() {
		return this.page.getByTestId('unavailable-resources-list');
	}

	getResourcesList() {
		return this.page.getByTestId('resources-list');
	}

	getEmptyResourcesList() {
		return this.page.getByTestId('empty-resources-list');
	}

	getEmptyResourcesListNewVariableButton() {
		return this.page.getByRole('button', { name: 'Add first variable' });
	}

	getSearchBar() {
		return this.page.getByTestId('resources-list-search');
	}

	getCreateVariableButton() {
		return this.page.getByTestId('add-resource-variable');
	}

	getVariablesRows() {
		return this.page.getByTestId('variables-row');
	}

	getVariableRow(key: string) {
		return this.getVariablesRows().filter({ hasText: key });
	}

	getEditableRowCancelButton(row: Locator) {
		return row.getByTestId('variable-row-cancel-button');
	}

	getEditableRowSaveButton(row: Locator) {
		return row.getByTestId('variable-row-save-button');
	}

	/**
	 * Create a variable with the key,
	 * @param key - The key of the variable
	 * @param value - The value of the variable
	 */

	async createVariableFromModal(
		key: string,
		value: string,
		{ shouldSave }: { shouldSave: boolean } = { shouldSave: true },
	) {
		await this.variableModal.waitForModal();
		await this.variableModal.addVariable(key, value, { shouldSave });
	}

	async createVariableFromEmptyState(key: string, value: string) {
		await this.getEmptyResourcesListNewVariableButton().click();
		await this.createVariableFromModal(key, value);
	}

	async createVariable(
		key: string,
		value: string,
		{ shouldSave }: { shouldSave: boolean } = { shouldSave: true },
	) {
		await this.getCreateVariableButton().click();
		await this.createVariableFromModal(key, value, { shouldSave });
	}

	async deleteVariable(key: string) {
		const row = this.getVariableRow(key);
		await row.getByTestId('variable-row-delete-button').click();

		// Use a more specific selector to avoid strict mode violation with other dialogs
		const modal = this.page.getByRole('dialog').filter({ hasText: 'Delete variable' });
		await expect(modal).toBeVisible();
		await modal.locator('.btn--confirm').click();
	}

	async editVariable(
		key: string,
		newValue: string,
		{ shouldSave }: { shouldSave: boolean } = { shouldSave: true },
	) {
		const row = this.getVariableRow(key);
		await row.getByTestId('variable-row-edit-button').click();
		await this.createVariableFromModal(key, newValue, { shouldSave });
	}
}
