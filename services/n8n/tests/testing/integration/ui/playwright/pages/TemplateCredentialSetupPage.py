"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/TemplateCredentialSetupPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage、./components/CredentialModal。导出:TemplateCredentialSetupPage。关键函数/方法:getTitle、getInfoCallout、getFormSteps、getStepHeading、getStepDescription、getSkipLink、getContinueButton、getCanvasSetupButton、getCanvasCredentialModal、getSetupCredentialModalCloseButton 等6项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/TemplateCredentialSetupPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/TemplateCredentialSetupPage.py

import type { Locator } from '@playwright/test';

import { BasePage } from './BasePage';
import { CredentialModal } from './components/CredentialModal';

export class TemplateCredentialSetupPage extends BasePage {
	readonly credentialModal = new CredentialModal(this.page.getByTestId('editCredential-modal'));
	getTitle(titleText: string): Locator {
		return this.page.getByRole('heading', { name: titleText, level: 1 });
	}

	getInfoCallout(): Locator {
		return this.page.getByTestId('info-callout');
	}

	getFormSteps(): Locator {
		return this.page.getByTestId('setup-credentials-form-step');
	}

	getStepHeading(step: Locator): Locator {
		return step.getByTestId('credential-step-heading');
	}

	getStepDescription(step: Locator): Locator {
		return step.getByTestId('credential-step-description');
	}

	getSkipLink(): Locator {
		return this.page.getByRole('link', { name: 'Skip' });
	}

	getContinueButton(): Locator {
		return this.page.getByTestId('continue-button');
	}

	getCanvasSetupButton(): Locator {
		return this.page.getByTestId('setup-credentials-button');
	}

	getCanvasCredentialModal(): Locator {
		return this.page.getByTestId('setup-workflow-credentials-modal');
	}

	getSetupCredentialModalCloseButton(): Locator {
		return this.page
			.getByTestId('setup-workflow-credentials-modal')
			.getByRole('button', { name: 'Close this dialog' });
	}

	getSetupCredentialModalSteps(): Locator {
		return this.page
			.getByTestId('setup-workflow-credentials-modal')
			.getByTestId('setup-credentials-form-step');
	}

	getCreateCredentialButton(appName: string): Locator {
		return this.page.getByRole('button', { name: `Create new ${appName} credential` });
	}

	getMessageBox(): Locator {
		// Using class selector as Element UI message box doesn't have semantic attributes
		return this.page.locator('.el-message-box');
	}

	/** Opens credential creation modal and waits for it to be visible */
	async openCredentialCreation(appName: string): Promise<void> {
		await this.getCreateCredentialButton(appName).click();
		await this.credentialModal.waitForModal();
	}

	/** Waits for the message box to appear and clicks the cancel button to dismiss it */
	async dismissMessageBox(): Promise<void> {
		const messageBox = this.getMessageBox();
		await messageBox.waitFor({ state: 'visible' });
		await messageBox.locator('.btn--cancel').click();
	}

	async closeSetupCredentialModal(): Promise<void> {
		await this.getSetupCredentialModalCloseButton().click();
		await this.getCanvasCredentialModal().waitFor({ state: 'hidden' });
	}
}
