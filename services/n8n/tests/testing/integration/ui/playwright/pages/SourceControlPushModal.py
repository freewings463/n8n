"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/SourceControlPushModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:@n8n/api-types；本地:无。导出:PushResult、SourceControlPushModal。关键函数/方法:getModal、getSubmitButton、push、getWorkflowsTab、getCredentialsTab、selectWorkflowsTab、selectCredentialsTab、isWorkflowsTabSelected、isCredentialsTabSelected、getFileInModal 等6项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/SourceControlPushModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/SourceControlPushModal.py

import type { GitCommitInfo, SourceControlledFile } from '@n8n/api-types';
import type { Locator, Page } from '@playwright/test';

export interface PushResult {
	files: SourceControlledFile[];
	commit: GitCommitInfo | null;
}

export class SourceControlPushModal {
	constructor(private readonly page: Page) {}

	getModal() {
		return this.page.getByTestId('sourceControlPush-modal');
	}

	getSubmitButton(): Locator {
		return this.page.getByTestId('source-control-push-modal-submit');
	}

	async push(commitMessage: string): Promise<PushResult> {
		await this.page.getByTestId('source-control-push-modal-commit').fill(commitMessage);

		const responsePromise = this.page.waitForResponse(
			(response) =>
				response.url().includes('/rest/source-control/push-workfolder') &&
				response.status() === 200,
		);

		await this.getSubmitButton().click();

		const response = await responsePromise;
		const json = await response.json();
		return json.data as PushResult;
	}

	// Tabs
	getWorkflowsTab(): Locator {
		return this.page.getByTestId('source-control-push-modal-tab-workflow');
	}

	getCredentialsTab(): Locator {
		return this.page.getByTestId('source-control-push-modal-tab-credential');
	}

	async selectWorkflowsTab(): Promise<void> {
		await this.getWorkflowsTab().click();
	}

	async selectCredentialsTab(): Promise<void> {
		await this.getCredentialsTab().click();
	}

	isWorkflowsTabSelected(): Promise<boolean> {
		return this.getWorkflowsTab()
			.getAttribute('class')
			.then((classList) => classList?.includes('tabActive') ?? false);
	}

	isCredentialsTabSelected(): Promise<boolean> {
		return this.getCredentialsTab()
			.getAttribute('class')
			.then((classList) => classList?.includes('tabActive') ?? false);
	}

	// File items
	getFileInModal(fileName: string): Locator {
		return this.getModal().getByTestId('push-modal-item').filter({ hasText: fileName }).first();
	}

	getFileCheckboxByName(fileName: string): Locator {
		// Find the checkbox that is associated with the file name
		return this.getModal()
			.locator('[data-test-id="source-control-push-modal-file-checkbox"]')
			.filter({ has: this.page.getByText(fileName, { exact: true }) });
	}

	async selectAllFilesInModal(): Promise<void> {
		const toggleAll = this.getModal().getByTestId('source-control-push-modal-toggle-all');
		const isChecked = await toggleAll.isChecked();
		if (!isChecked) {
			await toggleAll.click();
		}
	}

	getNotice(): Locator {
		return this.page.locator('#source-control-push-modal-notice.notice[role="alert"]');
	}

	getStatusBadge(fileName: string, status: 'New' | 'Modified' | 'Deleted'): Locator {
		return this.getFileCheckboxByName(fileName).getByText(status);
	}

	async deselectFile(fileName: string): Promise<void> {
		const checkbox = this.getFileCheckboxByName(fileName);
		const isChecked = await checkbox.isChecked();
		if (isChecked) {
			await checkbox.click();
		}
	}

	async selectFile(fileName: string): Promise<void> {
		const checkbox = this.getFileCheckboxByName(fileName);
		const isChecked = await checkbox.isChecked();
		if (!isChecked) {
			await checkbox.click();
		}
	}
}
