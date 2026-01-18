"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/ResourceCards.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:ResourceCards。关键函数/方法:getResourcesListWrapper、getFolders、getWorkflows、getCredentials、getFolder、getWorkflow、getCredential、getCardActionToggle、getCardAction、openCardActions 等4项。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/ResourceCards.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/ResourceCards.py

import type { Locator, Page } from '@playwright/test';

/**
 * ResourceCards component for handling folder, workflow, credential, and data store cards.
 * All cards are contained within a resources-list-wrapper.
 */
export class ResourceCards {
	constructor(private page: Page) {}

	getResourcesListWrapper(): Locator {
		return this.page.getByTestId('resources-list-wrapper');
	}

	getFolders(): Locator {
		return this.page.getByTestId('folder-card');
	}

	getWorkflows(): Locator {
		return this.page.getByTestId('resources-list-item-workflow');
	}

	getCredentials(): Locator {
		return this.page.getByTestId('resources-list-item');
	}

	getFolder(name: string): Locator {
		return this.page.locator(`[data-test-id="folder-card"][data-resourcename="${name}"]`);
	}

	getWorkflow(name: string): Locator {
		return this.getWorkflows().filter({ hasText: name });
	}

	getCredential(name: string): Locator {
		return this.getCredentials().filter({
			has: this.page.getByTestId('card-content').locator('h2').filter({ hasText: name }),
		});
	}

	getCardActionToggle(card: Locator): Locator {
		return card
			.getByTestId('card-append')
			.locator('[class*="action-toggle"]')
			.filter({ visible: true });
	}

	getCardAction(actionName: string): Locator {
		return this.page.getByTestId(`action-${actionName}`).filter({ visible: true });
	}

	async openCardActions(card: Locator): Promise<void> {
		await this.getCardActionToggle(card).click();
	}

	async clickCardAction(card: Locator, actionName: string): Promise<void> {
		await this.openCardActions(card);
		await this.getCardAction(actionName).click();
	}

	async openFolder(folderName: string): Promise<void> {
		const folderCard = this.getFolder(folderName);
		await this.clickCardAction(folderCard, 'open');
	}

	async deleteFolder(folderName: string): Promise<void> {
		const folderCard = this.getFolder(folderName);
		await this.clickCardAction(folderCard, 'delete');
	}

	async clickWorkflowCard(workflowName: string): Promise<void> {
		await this.getWorkflow(workflowName).getByTestId('card-content').click();
	}
}
