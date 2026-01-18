"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/SettingsUsersPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:SettingsUsersPage。关键函数/方法:search、getSearchInput、getRow、getInviteButton、getAccountType、clickAccountType、clickTransferUser、transferData、deleteData、selectAccountType 等2项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/SettingsUsersPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/SettingsUsersPage.py

import type { Locator } from '@playwright/test';

import { BasePage } from './BasePage';

export class SettingsUsersPage extends BasePage {
	getSearchInput(): Locator {
		return this.page.getByTestId('users-list-search');
	}

	getRow(email: string): Locator {
		return this.page.getByRole('row', { name: email });
	}

	getInviteButton() {
		return this.page.getByRole('button', { name: 'Invite' });
	}

	getAccountType(email: string) {
		return this.getRow(email).getByTestId('user-role-dropdown');
	}

	clickAccountType(email: string) {
		return this.getRow(email).getByTestId('user-role-dropdown').getByRole('button').click();
	}

	async search(email: string) {
		const searchInput = this.getSearchInput();
		await searchInput.click();
		await searchInput.fill(email);
	}

	async clickTransferUser(email: string) {
		await this.openActions(email);
		await this.page.getByTestId('action-transfer').click();
	}

	async transferData(email: string) {
		await this.page
			.getByRole('radio', {
				name: 'Transfer their workflows and credentials to another user or project',
			})
			// This doesn't work without force: true
			// eslint-disable-next-line playwright/no-force-option
			.click({ force: true });

		await this.page.getByPlaceholder('Select project or user').click();
		await this.page.getByTestId('project-sharing-info').filter({ hasText: email }).click();
		await this.page.getByRole('button', { name: 'Delete' }).click();
	}

	async deleteData() {
		await this.page
			.getByRole('radio', {
				name: 'Delete their workflows and credentials',
			})
			// This doesn't work without force: true
			// eslint-disable-next-line playwright/no-force-option
			.check({ force: true });
		await this.page.getByPlaceholder('delete all data').fill('delete all data');
		await this.page.getByRole('button', { name: 'Delete' }).click();
	}

	async selectAccountType(email: string, type: 'Admin' | 'Member') {
		await this.clickAccountType(email);
		await this.page.getByRole('menuitem', { name: type }).click();
	}

	async openActions(email: string) {
		await this.getRow(email).getByTestId('action-toggle').click();
	}

	async clickDeleteUser(email: string) {
		await this.openActions(email);
		await this.page.getByTestId('action-delete').filter({ visible: true }).click();
	}
}
