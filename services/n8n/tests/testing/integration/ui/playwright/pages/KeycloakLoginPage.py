"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/KeycloakLoginPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:KeycloakLoginPage。关键函数/方法:getUsernameField、getPasswordField、getLoginButton、fillUsername、fillPassword、clickLogin、login。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/KeycloakLoginPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/KeycloakLoginPage.py

import type { Locator } from '@playwright/test';

import { BasePage } from './BasePage';

/**
 * Page object for the Keycloak login page.
 * Used when testing OIDC authentication flows.
 */
export class KeycloakLoginPage extends BasePage {
	getUsernameField(): Locator {
		return this.page.locator('#username');
	}

	getPasswordField(): Locator {
		return this.page.locator('#password');
	}

	getLoginButton(): Locator {
		return this.page.locator('#kc-login');
	}

	async fillUsername(username: string): Promise<void> {
		await this.getUsernameField().fill(username);
	}

	async fillPassword(password: string): Promise<void> {
		await this.getPasswordField().fill(password);
	}

	async clickLogin(): Promise<void> {
		await this.getLoginButton().click();
	}

	/**
	 * Complete Keycloak login flow
	 * @param email - User email/username
	 * @param password - User password
	 */
	async login(email: string, password: string): Promise<void> {
		await this.getUsernameField().waitFor({ state: 'visible', timeout: 10000 });
		await this.fillUsername(email);
		await this.fillPassword(password);
		await this.clickLogin();
	}
}
