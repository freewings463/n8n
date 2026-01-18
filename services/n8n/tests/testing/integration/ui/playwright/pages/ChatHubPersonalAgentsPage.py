"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/ChatHubPersonalAgentsPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage、./components/ChatHubPersonalAgentModal、./components/ChatHubSidebar。导出:ChatHubPersonalAgentsPage。关键函数/方法:getNewAgentButton、getAgentCards、getEditButtonAt、getMenuAt。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/ChatHubPersonalAgentsPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/ChatHubPersonalAgentsPage.py

import type { Locator, Page } from '@playwright/test';

import { BasePage } from './BasePage';
import { ChatHubPersonalAgentModal } from './components/ChatHubPersonalAgentModal';
import { ChatHubSidebar } from './components/ChatHubSidebar';

export class ChatHubPersonalAgentsPage extends BasePage {
	readonly sidebar = new ChatHubSidebar(this.page.locator('#sidebar'));
	readonly editModal = new ChatHubPersonalAgentModal(
		this.page.getByTestId('agentEditorModal-modal'),
	);

	constructor(page: Page) {
		super(page);
	}

	getNewAgentButton(): Locator {
		return this.page.getByText('New Agent');
	}

	getAgentCards(): Locator {
		return this.page.getByTestId('chat-agent-card');
	}

	getEditButtonAt(index: number): Locator {
		return this.page.getByTestId('chat-agent-card').nth(index).getByTitle('Edit');
	}

	getMenuAt(index: number): Locator {
		return this.page.getByTestId('chat-agent-card').nth(index).getByTitle('More options');
	}
}
