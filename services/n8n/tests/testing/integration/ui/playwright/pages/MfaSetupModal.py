"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/MfaSetupModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:MfaSetupModal。关键函数/方法:getModalContainer、getTokenInput、getCopySecretToClipboardButton、getDownloadRecoveryCodesButton、getSaveButton、fillToken、clickCopySecretToClipboard、clickDownloadRecoveryCodes、clickSave、waitForHidden。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/MfaSetupModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/MfaSetupModal.py

import type { Locator } from '@playwright/test';
import { expect } from '@playwright/test';

import { BasePage } from './BasePage';

/**
 * Page object for the MFA setup modal that appears when enabling two-factor authentication.
 */
export class MfaSetupModal extends BasePage {
	getModalContainer(): Locator {
		return this.page.getByTestId('mfaSetup-modal');
	}

	getTokenInput(): Locator {
		return this.page.getByTestId('mfa-token-input');
	}

	getCopySecretToClipboardButton(): Locator {
		return this.page.getByTestId('mfa-secret-button');
	}

	getDownloadRecoveryCodesButton(): Locator {
		return this.page.getByTestId('mfa-recovery-codes-button');
	}

	getSaveButton(): Locator {
		return this.page.getByTestId('mfa-save-button');
	}

	async fillToken(token: string): Promise<void> {
		await this.getTokenInput().fill(token);
	}

	async clickCopySecretToClipboard(): Promise<void> {
		await this.clickByTestId('mfa-secret-button');
	}

	async clickDownloadRecoveryCodes(): Promise<void> {
		await this.clickByTestId('mfa-recovery-codes-button');
	}

	async clickSave(): Promise<void> {
		await this.getModalContainer().getByTestId('mfa-save-button').click();
	}

	/**
	 * Wait for the MFA setup modal to be hidden from view
	 */
	async waitForHidden(): Promise<void> {
		await expect(this.getModalContainer()).toBeHidden();
	}
}
