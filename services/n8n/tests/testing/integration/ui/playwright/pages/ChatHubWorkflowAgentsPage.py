"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/ChatHubWorkflowAgentsPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的工作流页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage、./components/ChatHubSidebar。导出:ChatHubWorkflowAgentsPage。关键函数/方法:getAgentCards、getEmptyText。用于组装工作流页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/ChatHubWorkflowAgentsPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/ChatHubWorkflowAgentsPage.py

import type { Locator, Page } from '@playwright/test';

import { BasePage } from './BasePage';
import { ChatHubSidebar } from './components/ChatHubSidebar';

export class ChatHubWorkflowAgentsPage extends BasePage {
	readonly sidebar = new ChatHubSidebar(this.page.locator('#sidebar'));

	constructor(page: Page) {
		super(page);
	}

	getAgentCards(): Locator {
		return this.page.getByTestId('chat-agent-card');
	}

	getEmptyText(): Locator {
		return this.page.getByText('No workflow agents available.');
	}
}
