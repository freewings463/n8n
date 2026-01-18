"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/MfaLoginPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:MfaLoginPage。关键函数/方法:getForm、getMfaCodeField、getMfaRecoveryCodeField、getEnterRecoveryCodeButton、getSubmitButton、goToMfaLogin、fillMfaCode、fillMfaRecoveryCode、clickEnterRecoveryCode、clickSubmit 等2项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/MfaLoginPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/MfaLoginPage.py

import type { Locator } from '@playwright/test';

import { BasePage } from './BasePage';

/**
 * Page object for the MFA login page that appears after entering email/password when MFA is enabled.
 */
export class MfaLoginPage extends BasePage {
	getForm(): Locator {
		return this.page.getByTestId('mfa-login-form');
	}

	getMfaCodeField(): Locator {
		return this.getForm().locator('input[name="mfaCode"]');
	}

	getMfaRecoveryCodeField(): Locator {
		return this.getForm().locator('input[name="mfaRecoveryCode"]');
	}

	getEnterRecoveryCodeButton(): Locator {
		return this.page.getByTestId('mfa-enter-recovery-code-button');
	}

	getSubmitButton(): Locator {
		return this.page.getByRole('button', { name: /^(Continue|Verify)$/ });
	}

	async goToMfaLogin(): Promise<void> {
		await this.page.goto('/mfa');
	}

	async fillMfaCode(code: string): Promise<void> {
		await this.getMfaCodeField().fill(code);
	}

	async fillMfaRecoveryCode(recoveryCode: string): Promise<void> {
		await this.getMfaRecoveryCodeField().fill(recoveryCode);
	}

	async clickEnterRecoveryCode(): Promise<void> {
		await this.clickByTestId('mfa-enter-recovery-code-button');
	}

	async clickSubmit(): Promise<void> {
		await this.getSubmitButton().click();
	}

	/**
	 * Fill MFA code and submit the form
	 * @param code - The MFA token to submit
	 */
	async submitMfaCode(code: string): Promise<void> {
		await this.fillMfaCode(code);
		// Form auto-submits
	}

	/**
	 * Switch to recovery code mode, fill recovery code and submit
	 * @param recoveryCode - The recovery code to submit
	 */
	async submitMfaRecoveryCode(recoveryCode: string): Promise<void> {
		await this.clickEnterRecoveryCode();
		await this.fillMfaRecoveryCode(recoveryCode);
		// Form auto-submits
	}
}
