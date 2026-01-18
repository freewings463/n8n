"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/ProjectSettingsPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:ProjectSettingsPage。关键函数/方法:fillProjectName、fillProjectDescription、clickSaveButton、clickCancelButton、getSaveButton、getCancelButton、getDeleteButton、getMembersSearchInput、getRoleDropdownFor、getMembersTable 等15项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/ProjectSettingsPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/ProjectSettingsPage.py

import { expect } from '@playwright/test';

import { BasePage } from './BasePage';

export class ProjectSettingsPage extends BasePage {
	async fillProjectName(name: string) {
		await this.page.getByTestId('project-settings-name-input').locator('input').fill(name);
	}

	async fillProjectDescription(description: string) {
		await this.page
			.getByTestId('project-settings-description-input')
			.locator('textarea')
			.fill(description);
	}

	async clickSaveButton() {
		await Promise.all([
			this.waitForRestResponse(/\/rest\/projects\/[^/]+$/, 'PATCH'),
			this.clickButtonByName('Save'),
		]);
	}

	async clickCancelButton() {
		await this.page.getByTestId('project-settings-cancel-button').click();
	}

	getSaveButton() {
		return this.page.getByTestId('project-settings-save-button');
	}

	getCancelButton() {
		return this.page.getByTestId('project-settings-cancel-button');
	}

	getDeleteButton() {
		return this.page.getByTestId('project-settings-delete-button');
	}

	getMembersSearchInput() {
		return this.page.getByPlaceholder('Add users...');
	}

	getRoleDropdownFor(email: string) {
		return this.getMembersTable()
			.locator('tr')
			.filter({ hasText: email })
			.getByTestId('project-member-role-dropdown')
			.getByRole('button');
	}

	getMembersTable() {
		return this.page.getByTestId('project-members-table');
	}

	async getMemberRowCount() {
		const table = this.getMembersTable();
		const rows = table.locator('tbody tr');
		return await rows.count();
	}

	async expectTableHasMemberCount(expectedCount: number) {
		const actualCount = await this.getMemberRowCount();
		expect(actualCount).toBe(expectedCount);
	}

	async expectSearchInputValue(expectedValue: string) {
		const searchInput = this.getMembersSearchInput();
		await expect(searchInput).toHaveValue(expectedValue);
	}

	getTitle() {
		return this.page.getByTestId('project-name');
	}

	// Robust value assertions on inner form controls
	getNameInput() {
		return this.page.locator('#projectName input');
	}

	getDescriptionTextarea() {
		return this.page.locator('#projectDescription textarea');
	}

	async expectProjectNameValue(value: string) {
		await expect(this.getNameInput()).toHaveValue(value);
	}

	async expectProjectDescriptionValue(value: string) {
		await expect(this.getDescriptionTextarea()).toHaveValue(value);
	}

	async expectTableIsVisible() {
		const table = this.getMembersTable();
		await expect(table).toBeVisible();
	}

	async expectMembersSelectIsVisible() {
		const select = this.page.getByTestId('project-members-select');
		await expect(select).toBeVisible();
	}

	// Icon picker methods
	getIconPickerButton() {
		return this.page.getByTestId('icon-picker-button');
	}

	async clickIconPickerButton() {
		await this.getIconPickerButton().click();
	}

	async selectIconTab(tabName: string) {
		await this.page.getByTestId('icon-picker-tabs').getByText(tabName).click();
	}

	async selectFirstEmoji() {
		await this.page.getByTestId('icon-picker-emoji').first().click();
	}
}
