"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/SourceControlPullModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:SourceControlPullModal。关键函数/方法:getModal、getPullAndOverrideButton、pull、getWorkflowsTab、getCredentialsTab、selectWorkflowsTab、selectCredentialsTab、getFileInModal、getStatusBadge、getNotice。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/SourceControlPullModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/SourceControlPullModal.py

import type { Locator, Page } from '@playwright/test';

export class SourceControlPullModal {
	constructor(private readonly page: Page) {}

	getModal() {
		return this.page.getByTestId('sourceControlPull-modal');
	}

	getPullAndOverrideButton(): Locator {
		return this.page.getByTestId('force-pull');
	}

	async pull(): Promise<void> {
		await this.getPullAndOverrideButton().click();
	}

	getWorkflowsTab(): Locator {
		return this.page.getByTestId('source-control-pull-modal-tab-workflow');
	}

	getCredentialsTab(): Locator {
		return this.page.getByTestId('source-control-pull-modal-tab-credential');
	}

	async selectWorkflowsTab(): Promise<void> {
		await this.getWorkflowsTab().click();
	}

	async selectCredentialsTab(): Promise<void> {
		await this.getCredentialsTab().click();
	}

	getFileInModal(fileName: string): Locator {
		return this.page.getByTestId('pull-modal-item').filter({ hasText: fileName }).first();
	}

	getStatusBadge(fileName: string, status: 'New' | 'Modified' | 'Deleted' | 'Conflict'): Locator {
		return this.getFileInModal(fileName).getByText(status, { exact: true });
	}

	getNotice(): Locator {
		return this.page.locator('[class*="notice"]');
	}
}
