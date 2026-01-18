"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/BasePage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./components/BaseModal、./components/FloatingUiHelper。导出:无。关键函数/方法:clickByTestId、fillByTestId、clickByText、clickButtonByName、waitForRestResponse。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/BasePage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/BasePage.py

import type { Page } from '@playwright/test';

import { BaseModal } from './components/BaseModal';
import { FloatingUiHelper } from './components/FloatingUiHelper';

export abstract class BasePage extends FloatingUiHelper {
	protected readonly baseModal: BaseModal;

	constructor(protected readonly page: Page) {
		super(page);
		this.baseModal = new BaseModal(this.page);
	}

	protected async clickByTestId(testId: string) {
		await this.page.getByTestId(testId).click();
	}

	protected async fillByTestId(testId: string, value: string) {
		await this.page.getByTestId(testId).fill(value);
	}

	protected async clickByText(text: string) {
		await this.page.getByText(text).click();
	}

	protected async clickButtonByName(name: string) {
		await this.page.getByRole('button', { name }).click();
	}

	protected async waitForRestResponse(
		url: string | RegExp,
		method?: 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE',
	) {
		if (typeof url === 'string') {
			return await this.page.waitForResponse((res) => {
				const matches = res.url().includes(url);
				return matches && (method ? res.request().method() === method : true);
			});
		}

		return await this.page.waitForResponse((res) => {
			const matches = url.test(res.url());
			return matches && (method ? res.request().method() === method : true);
		});
	}
}
