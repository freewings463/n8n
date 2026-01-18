"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/SignInPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:SignInPage。关键函数/方法:getForm、getEmailField、getPasswordField、getSubmitButton、getSsoButton、goToSignIn、fillEmail、fillPassword、clickSubmit、loginWithEmailAndPassword。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/SignInPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/SignInPage.py

import type { Locator } from '@playwright/test';

import { BasePage } from './BasePage';

export class SignInPage extends BasePage {
	getForm(): Locator {
		return this.page.getByTestId('auth-form');
	}

	getEmailField(): Locator {
		return this.page.getByTestId('emailOrLdapLoginId').locator('input');
	}

	getPasswordField(): Locator {
		return this.page.getByTestId('password').locator('input');
	}

	getSubmitButton(): Locator {
		return this.page.getByTestId('form-submit-button');
	}

	getSsoButton(): Locator {
		return this.page.getByRole('button', { name: /continue with sso/i });
	}

	async goToSignIn(): Promise<void> {
		await this.page.goto('/signin');
	}

	async fillEmail(email: string): Promise<void> {
		await this.getEmailField().fill(email);
	}

	async fillPassword(password: string): Promise<void> {
		await this.getPasswordField().fill(password);
	}

	async clickSubmit(): Promise<void> {
		await this.getSubmitButton().click();
	}

	/**
	 * Complete login flow with email and password
	 * @param email - User email
	 * @param password - User password
	 * @param waitForWorkflow - Whether to wait for redirect to workflow page after login
	 */
	async loginWithEmailAndPassword(
		email: string,
		password: string,
		waitForWorkflow = false,
	): Promise<void> {
		await this.goToSignIn();
		await this.fillEmail(email);
		await this.fillPassword(password);
		await this.clickSubmit();

		if (waitForWorkflow) {
			await this.page.waitForURL(/workflows/);
		}
	}
}
