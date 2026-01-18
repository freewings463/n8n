"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/SettingsEnvironmentPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:SettingsEnvironmentPage。关键函数/方法:getConnectButton、getDisconnectButton、getSSHKeyValue、getRepoUrlInput、getBranchSelect、getSaveButton、fillRepoUrl、selectBranch、enableReadOnlyMode、disableReadOnlyMode 等1项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/SettingsEnvironmentPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/SettingsEnvironmentPage.py

import { expect, type Locator } from '@playwright/test';

import { BasePage } from './BasePage';

export class SettingsEnvironmentPage extends BasePage {
	getConnectButton(): Locator {
		return this.page.getByTestId('source-control-connect-button');
	}

	getDisconnectButton(): Locator {
		return this.page.getByTestId('source-control-disconnect-button');
	}

	getSSHKeyValue(): Locator {
		return this.page.getByTestId('copy-input').locator('span').first();
	}

	getRepoUrlInput(): Locator {
		return this.page.getByPlaceholder('git@github.com:user/repository.git');
	}

	getBranchSelect(): Locator {
		return this.page.getByTestId('source-control-branch-select');
	}

	getSaveButton(): Locator {
		return this.page.getByTestId('source-control-save-settings-button');
	}

	fillRepoUrl(url: string): Promise<void> {
		return this.getRepoUrlInput().fill(url);
	}

	async selectBranch(branchName: string): Promise<void> {
		await this.getBranchSelect().click();
		await this.page.getByRole('option', { name: branchName }).click();
	}

	async enableReadOnlyMode(): Promise<void> {
		const checkbox = this.page.getByTestId('source-control-read-only-checkbox');
		await checkbox.check();
	}

	async disableReadOnlyMode(): Promise<void> {
		const checkbox = this.page.getByTestId('source-control-read-only-checkbox');
		await checkbox.uncheck();
	}

	async disconnect(): Promise<void> {
		await this.getDisconnectButton().click();

		const confirmModal = this.page
			.getByRole('dialog')
			.filter({ hasText: 'Disconnect Git repository' });
		await expect(confirmModal).toBeVisible();
		await confirmModal.locator('.btn--confirm').click();
	}
}
