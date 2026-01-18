"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/ResourceMoveModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:ResourceMoveModal。关键函数/方法:getProjectSelect、getProjectSelectCredential、getMoveConfirmButton、getMoveCredentialButton、getFolderSelect、selectProjectOption、clickMoveCredentialButton、clickConfirmMoveButton。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/ResourceMoveModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/ResourceMoveModal.py

import type { Locator, Page } from '@playwright/test';

/**
 * Page object for interacting with move resource modals (MoveToFolderModal for workflows, ProjectMoveResourceModal for credentials).
 */
export class ResourceMoveModal {
	constructor(private page: Page) {}

	getProjectSelect(): Locator {
		return this.page.getByTestId('project-sharing-select');
	}

	getProjectSelectCredential(): Locator {
		return this.page.getByTestId('project-move-resource-modal-select');
	}

	getMoveConfirmButton(): Locator {
		return this.page.getByTestId('confirm-move-folder-button');
	}

	getMoveCredentialButton(): Locator {
		return this.page.getByRole('button', { name: 'Move credential' });
	}

	getFolderSelect(): Locator {
		return this.page.getByTestId('move-to-folder-dropdown');
	}

	async selectProjectOption(projectNameOrEmail: string): Promise<void> {
		await this.page.getByRole('option').filter({ hasText: projectNameOrEmail }).click();
	}

	async clickMoveCredentialButton(): Promise<void> {
		await this.getMoveCredentialButton().click();
	}

	async clickConfirmMoveButton(): Promise<void> {
		await this.getMoveConfirmButton().click();
	}
}
