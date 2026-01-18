"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/AddResource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:AddResource。关键函数/方法:getWorkflowButton、getAction、workflow、credential、folder、dataTable。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/AddResource.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/AddResource.py

import type { Locator, Page } from '@playwright/test';

/**
 * AddResource component for creating workflows, credentials, folders, and data tables.
 * Represents the "add resource" functionality in the project header.
 *
 * @example
 * // Access via workflows page
 * await n8n.workflows.addResource.workflow();
 * await n8n.workflows.addResource.credential();
 * await n8n.workflows.addResource.folder();
 * await n8n.workflows.addResource.dataTable();
 */
export class AddResource {
	constructor(private page: Page) {}

	getWorkflowButton(): Locator {
		return this.page.getByTestId('add-resource-workflow');
	}

	getAction(actionType: string): Locator {
		return this.page.getByTestId(`action-${actionType}`);
	}

	async workflow(): Promise<void> {
		await this.getWorkflowButton().click();
	}

	async credential(): Promise<void> {
		await this.page.getByTestId('add-resource-credential').click();
	}

	async folder(): Promise<void> {
		await this.page.getByTestId('add-resource').click();
		await this.page.getByTestId('action-folder').click();
	}

	async dataTable(fromDataTableTab: boolean = true): Promise<void> {
		if (fromDataTableTab) {
			await this.page.getByTestId('add-resource-dataTable').click();
		} else {
			await this.page.getByTestId('add-resource').click();
			await this.page.getByTestId('action-dataTable').click();
		}
	}
}
