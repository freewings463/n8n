"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/ChatHubSidebar.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:ChatHubSidebar。关键函数/方法:getPersonalAgentButton、getWorkflowAgentButton、getConversations。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/ChatHubSidebar.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/ChatHubSidebar.py

import type { Locator } from '@playwright/test';

export class ChatHubSidebar {
	constructor(private root: Locator) {}

	getPersonalAgentButton() {
		return this.root.getByRole('menuitem', { name: 'Personal agents' });
	}

	getWorkflowAgentButton() {
		return this.root.getByRole('menuitem', { name: 'Workflow agents' });
	}

	getConversations() {
		return this.root.getByTestId('chat-conversation-list').getByRole('link');
	}
}
