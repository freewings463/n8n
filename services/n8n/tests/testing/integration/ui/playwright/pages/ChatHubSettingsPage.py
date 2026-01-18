"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/ChatHubSettingsPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage、./components/ChatHubProviderSettingsModal、./components/CredentialModal。导出:ChatHubSettingsPage。关键函数/方法:getProvidersTable、getProviderRow、getProviderActionToggle。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/ChatHubSettingsPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/ChatHubSettingsPage.py

import type { Locator, Page } from '@playwright/test';

import { BasePage } from './BasePage';
import { ChatHubProviderSettingsModal } from './components/ChatHubProviderSettingsModal';
import { CredentialModal } from './components/CredentialModal';

export class ChatHubSettingsPage extends BasePage {
	readonly providerModal = new ChatHubProviderSettingsModal(
		this.page.getByTestId('chatProviderSettingsModal-modal'),
	);
	readonly credentialModal = new CredentialModal(this.page.getByTestId('editCredential-modal'));

	constructor(page: Page) {
		super(page);
	}

	getProvidersTable(): Locator {
		return this.page.getByTestId('chat-providers-table');
	}

	getProviderRow(providerName: string): Locator {
		return this.getProvidersTable().getByRole('row').filter({ hasText: providerName });
	}

	getProviderActionToggle(providerName: string): Locator {
		return this.getProviderRow(providerName).getByTestId('action-toggle');
	}
}
