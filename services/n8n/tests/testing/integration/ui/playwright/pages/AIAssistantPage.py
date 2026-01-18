"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/AIAssistantPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:无；内部:无；本地:./BasePage。导出:AIAssistantPage。关键函数/方法:getAskAssistantFloatingButton、getAskAssistantCanvasActionButton、getAskAssistantChat、getAskAssistantSidebar、getPlaceholderMessage、getChatInput、getSendMessageButton、getCloseChatButton、getAskAssistantSidebarResizer、getNodeErrorViewAssistantButton 等15项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/AIAssistantPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/AIAssistantPage.py

import { BasePage } from './BasePage';

export class AIAssistantPage extends BasePage {
	// #region Getters

	getAskAssistantFloatingButton() {
		return this.page.getByTestId('ask-assistant-floating-button');
	}

	getAskAssistantCanvasActionButton() {
		return this.page.getByTestId('ask-assistant-canvas-action-button');
	}

	getAskAssistantChat() {
		return this.page.getByTestId('ask-assistant-chat');
	}

	getAskAssistantSidebar() {
		return this.page.getByTestId('ask-assistant-sidebar');
	}

	getPlaceholderMessage() {
		return this.page.getByTestId('placeholder-message');
	}

	getChatInput() {
		// Try suggestions input first (shown when suggestions are visible),
		// fall back to regular input (shown when there are messages)
		const suggestionsInput = this.page.getByTestId('chat-suggestions-input').locator('textarea');
		const regularInput = this.page.getByTestId('chat-input').locator('textarea');

		// Return the first one that's visible
		return suggestionsInput.or(regularInput);
	}

	getSendMessageButton() {
		return this.page.getByTestId('send-message-button');
	}

	getCloseChatButton() {
		return this.page.getByTestId('close-chat-button');
	}

	getAskAssistantSidebarResizer() {
		return this.getAskAssistantSidebar().locator('[class*="_resizer"][data-dir="left"]').first();
	}

	getNodeErrorViewAssistantButton() {
		return this.page.getByTestId('node-error-view-ask-assistant-button').locator('button').first();
	}

	getChatMessagesAll() {
		return this.page.locator('[data-test-id^="chat-message"]');
	}

	getChatMessagesAssistant() {
		return this.page.getByTestId('chat-message-assistant');
	}

	getChatMessagesUser() {
		return this.page.getByTestId('chat-message-user');
	}

	getChatMessagesSystem() {
		return this.page.getByTestId('chat-message-system');
	}

	getQuickReplyButtons() {
		return this.page.getByTestId('quick-replies').locator('button');
	}

	getQuickReplies() {
		return this.page.getByTestId('quick-replies');
	}

	getNewAssistantSessionModal() {
		return this.page.getByTestId('new-assistant-session-modal');
	}

	getCodeDiffs() {
		return this.page.getByTestId('code-diff-suggestion');
	}

	getApplyCodeDiffButtons() {
		return this.page.getByTestId('replace-code-button');
	}

	getUndoReplaceCodeButtons() {
		return this.page.getByTestId('undo-replace-button');
	}

	getCodeReplacedMessage() {
		return this.page.getByTestId('code-replaced-message');
	}

	getCredentialEditAssistantButton() {
		return this.page.getByTestId('credential-edit-ask-assistant-button');
	}

	getCodeSnippet() {
		return this.page.getByTestId('assistant-code-snippet-content');
	}

	// #endregion

	// #region Actions

	async sendMessage(
		message: string,
		method: 'send-message-button' | 'enter-key' = 'send-message-button',
	) {
		// Only type if there's a message to type (e.g., skip for pre-populated suggestion pills)
		if (message) {
			await this.getChatInput().pressSequentially(message, { delay: 20 });
		}
		if (method === 'enter-key') {
			await this.getChatInput().press('Enter');
		} else {
			await this.getSendMessageButton().click();
		}
	}

	async waitForStreamingComplete(options?: { timeout?: number }) {
		const timeout = options?.timeout ?? 60000;
		// Wait for at least one assistant message to appear (indicating streaming has produced output)
		// and ensure the send button is re-enabled (indicating streaming is complete)
		await this.getChatMessagesAssistant().first().waitFor({ state: 'visible', timeout });
		await this.page.waitForFunction(
			() => {
				const sendButton = document.querySelector(
					'[data-test-id="send-message-button"]',
				) as HTMLButtonElement;
				return sendButton && !sendButton.disabled;
			},
			{ timeout },
		);
	}

	// #endregion
}
