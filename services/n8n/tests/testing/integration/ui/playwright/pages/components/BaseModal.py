"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/BaseModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:./FloatingUiHelper。导出:BaseModal。关键函数/方法:getCloseButton、waitForModal、waitForModalToClose、fillInput、clickButton、getTitle、getMessage。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/BaseModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/BaseModal.py

import type { Page } from '@playwright/test';

import { FloatingUiHelper } from './FloatingUiHelper';

/**
 * Base modal component for handling modal dialogs.
 */
export class BaseModal extends FloatingUiHelper {
	constructor(protected readonly page: Page) {
		super(page);
	}

	get container() {
		return this.page.getByRole('dialog');
	}

	getCloseButton() {
		return this.container.getByRole('button', { name: /close/i });
	}

	async waitForModal() {
		await this.container.waitFor({ state: 'visible' });
	}

	async waitForModalToClose() {
		await this.container.waitFor({ state: 'hidden' });
	}

	async fillInput(text: string) {
		await this.container.getByRole('textbox').fill(text);
	}

	async clickButton(buttonText: string | RegExp) {
		await this.container.getByRole('button', { name: buttonText }).click();
	}

	async getTitle() {
		return await this.container.getByRole('heading').textContent();
	}

	async getMessage() {
		return await this.container.textContent();
	}
}
