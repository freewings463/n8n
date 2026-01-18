"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/WorkflowSettingsModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的工作流页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:WorkflowSettingsModal。关键函数/方法:getModal、getWorkflowMenu、getSettingsMenuItem、getErrorWorkflowField、getTimezoneField、getSaveFailedExecutionsField、getSaveSuccessExecutionsField、getSaveManualExecutionsField、getSaveExecutionProgressField、getTimeoutSwitch 等23项。用于组装工作流页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/WorkflowSettingsModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/WorkflowSettingsModal.py

import type { Locator } from '@playwright/test';

import { BasePage } from './BasePage';

export class WorkflowSettingsModal extends BasePage {
	getModal(): Locator {
		return this.page.getByTestId('workflow-settings-dialog');
	}

	getWorkflowMenu(): Locator {
		return this.page.getByTestId('workflow-menu');
	}

	getSettingsMenuItem(): Locator {
		return this.page.getByTestId('workflow-menu-item-settings');
	}

	getErrorWorkflowField(): Locator {
		return this.page.getByTestId('workflow-settings-error-workflow');
	}

	getTimezoneField(): Locator {
		return this.page.getByTestId('workflow-settings-timezone');
	}

	getSaveFailedExecutionsField(): Locator {
		return this.page.getByTestId('workflow-settings-save-failed-executions');
	}

	getSaveSuccessExecutionsField(): Locator {
		return this.page.getByTestId('workflow-settings-save-success-executions');
	}

	getSaveManualExecutionsField(): Locator {
		return this.page.getByTestId('workflow-settings-save-manual-executions');
	}

	getSaveExecutionProgressField(): Locator {
		return this.page.getByTestId('workflow-settings-save-execution-progress');
	}

	getTimeoutSwitch(): Locator {
		return this.page.getByTestId('workflow-settings-timeout-workflow');
	}

	getTimeoutInput(): Locator {
		return this.page.getByTestId('workflow-settings-timeout-form').locator('input').first();
	}

	getDuplicateMenuItem(): Locator {
		return this.page.getByTestId('workflow-menu-item-duplicate');
	}

	getDeleteMenuItem(): Locator {
		return this.page.getByTestId('workflow-menu-item-delete');
	}

	getArchiveMenuItem(): Locator {
		return this.page.getByTestId('workflow-menu-item-archive');
	}

	getUnarchiveMenuItem(): Locator {
		return this.page.getByTestId('workflow-menu-item-unarchive');
	}

	getPushToGitMenuItem(): Locator {
		return this.page.getByTestId('workflow-menu-item-push');
	}

	getUnpublishMenuItem(): Locator {
		return this.page.getByTestId('workflow-menu-item-unpublish');
	}

	getUnpublishModal(): Locator {
		return this.page.getByTestId('workflow-history-version-unpublish-modal');
	}

	async clickUnpublishMenuItem(): Promise<void> {
		await this.getUnpublishMenuItem().click();
	}

	async confirmUnpublishModal(): Promise<void> {
		await this.getUnpublishModal().getByRole('button', { name: 'Unpublish' }).click();
	}

	getSaveButton(): Locator {
		return this.page.getByRole('button', { name: 'Save' });
	}

	getDuplicateModal(): Locator {
		return this.page.getByTestId('duplicate-modal');
	}

	getDuplicateNameInput(): Locator {
		return this.getDuplicateModal().locator('input').first();
	}

	getDuplicateTagsInput(): Locator {
		return this.getDuplicateModal().locator('.el-select__tags input');
	}

	getDuplicateSaveButton(): Locator {
		return this.getDuplicateModal().getByRole('button', { name: /duplicate|save/i });
	}

	async open(): Promise<void> {
		await this.getWorkflowMenu().click();
		await this.getSettingsMenuItem().click();
	}

	async clickSave(): Promise<void> {
		await this.getSaveButton().click();
	}

	async selectErrorWorkflow(workflowName: string): Promise<void> {
		await this.getErrorWorkflowField().click();
		await this.page.getByRole('option', { name: workflowName }).first().click();
	}

	async clickArchiveMenuItem(): Promise<void> {
		await this.getArchiveMenuItem().click();
	}

	async clickUnarchiveMenuItem(): Promise<void> {
		await this.getUnarchiveMenuItem().click();
	}

	async clickDeleteMenuItem(): Promise<void> {
		await this.getDeleteMenuItem().click();
	}

	async confirmDeleteModal(): Promise<void> {
		await this.page.getByRole('button', { name: 'delete' }).click();
	}

	async confirmArchiveModal(): Promise<void> {
		await this.page.locator('.btn--confirm').click();
	}
}
