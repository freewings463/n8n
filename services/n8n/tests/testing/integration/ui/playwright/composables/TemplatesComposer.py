"""
MIGRATION-META:
  source_path: packages/testing/playwright/composables/TemplatesComposer.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/composables 的组合式函数。导入/依赖:外部:@playwright/test；内部:无；本地:../pages/n8nPage。导出:TemplatesComposer。关键函数/方法:importFirstTemplate、fillDummyCredentialForApp、fillDummyCredentialForAppWithConfirm。用于封装该模块复用逻辑（hooks/composables）供组件组合。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/composables/TemplatesComposer.ts -> services/n8n/tests/testing/integration/ui/playwright/composables/TemplatesComposer.py

import { expect } from '@playwright/test';

import type { n8nPage } from '../pages/n8nPage';

/**
 * A class for user interactions with templates that go across multiple pages.
 */
export class TemplatesComposer {
	constructor(private readonly n8n: n8nPage) {}

	/**
	 * Navigates to templates page, waits for loading to complete,
	 * selects the first available template, and imports it to a new workflow
	 * @returns Promise that resolves when the template has been imported
	 */
	async importFirstTemplate(): Promise<void> {
		await this.n8n.navigate.toTemplates();
		await expect(this.n8n.templates.getSkeletonLoader()).toBeHidden();
		await expect(this.n8n.templates.getFirstTemplateCard()).toBeVisible();
		await expect(this.n8n.templates.getTemplatesLoadingContainer()).toBeHidden();

		await this.n8n.templates.clickFirstTemplateCard();
		await expect(this.n8n.templates.getUseTemplateButton()).toBeVisible();

		await this.n8n.templates.clickUseTemplateButton();
		// New workflows redirect to /workflow/<id>?new=true with optional templateId
		await expect(this.n8n.page).toHaveURL(/\/workflow\/[a-zA-Z0-9_-]+\?.*new=true/);
	}

	/**
	 * Fill in dummy credentials for an app in the template credential setup flow
	 * Opens credential creation, fills name, saves, and closes modal
	 * @param appName - The name of the app (e.g. 'Shopify', 'X (Formerly Twitter)')
	 */
	async fillDummyCredentialForApp(
		appName: string,
		{ fields }: { fields: Record<string, string> } = { fields: {} },
	): Promise<void> {
		await this.n8n.templateCredentialSetup.openCredentialCreation(appName);
		await this.n8n.templateCredentialSetup.credentialModal.getCredentialName().click();
		await this.n8n.templateCredentialSetup.credentialModal.getNameInput().fill('test');
		await this.n8n.templateCredentialSetup.credentialModal.fillAllFields(fields);
		await this.n8n.templateCredentialSetup.credentialModal.save();
		await this.n8n.templateCredentialSetup.credentialModal.close();
	}

	/**
	 * Fill in dummy credentials for an app and handle confirmation dialog
	 * @param appName - The name of the app
	 */
	async fillDummyCredentialForAppWithConfirm(
		appName: string,
		{ fields }: { fields: Record<string, string> } = { fields: {} },
	): Promise<void> {
		await this.fillDummyCredentialForApp(appName, { fields });
		await this.n8n.templateCredentialSetup.dismissMessageBox();
	}
}
