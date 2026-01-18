"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/CommunityNodesPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:CommunityNodesPage。关键函数/方法:getCommunityCards、getActionBox、getInstallButton、getInstallModal、getConfirmModal、getPackageNameInput、getUserAgreementCheckbox、getInstallPackageButton、getActionToggle、getUninstallAction 等15项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/CommunityNodesPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/CommunityNodesPage.py

import type { Locator } from '@playwright/test';

import { BasePage } from './BasePage';

export class CommunityNodesPage extends BasePage {
	// Element getters
	getCommunityCards(): Locator {
		return this.page.getByTestId('community-package-card');
	}

	getActionBox(): Locator {
		return this.page.getByTestId('action-box');
	}

	getInstallButton(): Locator {
		// Try action box first (empty state), fallback to header install button
		const actionBoxButton = this.getActionBox().locator('button');
		const headerInstallButton = this.page.getByRole('button', { name: 'Install' });

		return actionBoxButton.or(headerInstallButton);
	}

	getInstallModal(): Locator {
		return this.page.getByTestId('communityPackageInstall-modal');
	}

	getConfirmModal(): Locator {
		return this.page.getByTestId('communityPackageManageConfirm-modal');
	}

	getPackageNameInput(): Locator {
		return this.getInstallModal().locator('input').first();
	}

	getUserAgreementCheckbox(): Locator {
		return this.page.getByTestId('user-agreement-checkbox');
	}

	getInstallPackageButton(): Locator {
		return this.page.getByTestId('install-community-package-button');
	}

	getActionToggle(): Locator {
		return this.page.getByTestId('action-toggle');
	}

	getUninstallAction(): Locator {
		return this.page.getByTestId('action-uninstall');
	}

	getUpdateButton(): Locator {
		return this.getCommunityCards().first().locator('button');
	}

	getConfirmUpdateButton(): Locator {
		return this.getConfirmModal().getByRole('button', { name: 'Confirm update' });
	}

	getConfirmUninstallButton(): Locator {
		return this.getConfirmModal().getByRole('button', { name: 'Confirm uninstall' });
	}

	// Simple actions
	async clickInstallButton(): Promise<void> {
		await this.getInstallButton().click();
	}

	async fillPackageName(packageName: string): Promise<void> {
		await this.getPackageNameInput().fill(packageName);
	}

	async clickUserAgreementCheckbox(): Promise<void> {
		await this.getUserAgreementCheckbox().click();
	}

	async clickInstallPackageButton(): Promise<void> {
		await this.getInstallPackageButton().click();
	}

	async clickActionToggle(): Promise<void> {
		await this.getActionToggle().click();
	}

	async clickUninstallAction(): Promise<void> {
		await this.getUninstallAction().click();
	}

	async clickUpdateButton(): Promise<void> {
		await this.getUpdateButton().click();
	}

	async clickConfirmUpdate(): Promise<void> {
		await this.getConfirmUpdateButton().click();
	}

	async clickConfirmUninstall(): Promise<void> {
		await this.getConfirmUninstallButton().click();
	}

	// Helper methods for common workflows
	async installPackage(packageName: string): Promise<void> {
		await this.clickInstallButton();
		await this.fillPackageName(packageName);
		await this.clickUserAgreementCheckbox();
		await this.clickInstallPackageButton();

		// Wait for install modal to close
		await this.getInstallModal().waitFor({ state: 'hidden' });
	}

	async updatePackage(): Promise<void> {
		await this.clickUpdateButton();
		await this.clickConfirmUpdate();
	}

	async uninstallPackage(): Promise<void> {
		await this.clickActionToggle();
		await this.clickUninstallAction();
		await this.clickConfirmUninstall();
	}
}
