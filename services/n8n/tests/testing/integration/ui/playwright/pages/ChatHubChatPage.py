"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/ChatHubChatPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage、./components/ChatHubCredentialModal、./components/ChatHubPersonalAgentModal 等2项。导出:ChatHubChatPage。关键函数/方法:getGreetingMessage、getModelSelectorButton、getSelectedCredentialName、getChatInput、getSendButton、getChatMessages、getEditButtonAt、getEditorAt、getSendButtonAt、getRegenerateButtonAt 等9项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/ChatHubChatPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/ChatHubChatPage.py

import type { Locator, Page } from '@playwright/test';

import { BasePage } from './BasePage';
import { ChatHubCredentialModal } from './components/ChatHubCredentialModal';
import { ChatHubPersonalAgentModal } from './components/ChatHubPersonalAgentModal';
import { ChatHubSidebar } from './components/ChatHubSidebar';
import { ChatHubToolsModal } from './components/ChatHubToolsModal';

export class ChatHubChatPage extends BasePage {
	readonly sidebar = new ChatHubSidebar(this.page.locator('#sidebar'));
	readonly toolsModal = new ChatHubToolsModal(this.page.getByTestId('toolsSelectorModal-modal'));
	readonly credModal = new ChatHubCredentialModal(
		this.page.getByTestId('chatCredentialSelectorModal-modal'),
	);
	readonly personalAgentModal = new ChatHubPersonalAgentModal(
		this.page.getByTestId('agentEditorModal-modal'),
	);

	constructor(page: Page) {
		super(page);
	}

	getGreetingMessage(): Locator {
		return this.page.getByRole('heading', { level: 2 });
	}

	getModelSelectorButton(): Locator {
		return this.page.getByTestId('chat-model-selector');
	}

	getSelectedCredentialName(): Locator {
		return this.getModelSelectorButton().locator('span');
	}

	getChatInput(): Locator {
		return this.page.locator('form').getByRole('textbox');
	}

	getSendButton(): Locator {
		return this.page.getByTitle('Send');
	}

	getChatMessages(): Locator {
		return this.page.locator('[data-message-id]');
	}

	getEditButtonAt(index: number): Locator {
		return this.getChatMessages().nth(index).getByTestId('chat-message-edit');
	}

	getEditorAt(index: number): Locator {
		return this.getChatMessages().nth(index).getByRole('textbox');
	}

	getSendButtonAt(index: number): Locator {
		return this.getChatMessages().nth(index).getByText('Send');
	}

	getRegenerateButtonAt(index: number): Locator {
		return this.getChatMessages().nth(index).getByTestId('chat-message-regenerate');
	}

	getPrevAlternativeButtonAt(index: number): Locator {
		return this.getChatMessages().nth(index).getByTestId('chat-message-prev-alternative');
	}

	getNextAlternativeButtonAt(index: number): Locator {
		return this.getChatMessages().nth(index).getByTestId('chat-message-next-alternative');
	}

	getAttachButton(): Locator {
		return this.page.getByRole('button', { name: /attach/i });
	}

	getFileInput(): Locator {
		return this.page.locator('input[type="file"]');
	}

	getAttachmentsAt(messageIndex: number): Locator {
		return this.getChatMessages().nth(messageIndex).locator('.chat-file');
	}

	getToolsButton(): Locator {
		return this.page.locator('[class*="toolsButton"]');
	}

	getOpenWorkflowButton(): Locator {
		return this.page.getByRole('button', { name: /open workflow/i });
	}

	async clickOpenWorkflowButton(): Promise<Page> {
		const newPagePromise = this.page.context().waitForEvent('page');

		await this.getOpenWorkflowButton().click();

		const workflowPage = await newPagePromise;

		await workflowPage.waitForLoadState();
		return workflowPage;
	}

	async openAttachmentAt(messageIndex: number, attachmentIndex: number): Promise<Page> {
		const [newPage] = await Promise.all([
			this.page.context().waitForEvent('page'),
			this.getAttachmentsAt(messageIndex).nth(attachmentIndex).click(),
		]);

		await newPage.waitForLoadState('load');

		return newPage;
	}
}
