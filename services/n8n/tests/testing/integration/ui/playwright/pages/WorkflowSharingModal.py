"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/WorkflowSharingModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的工作流页面。导入/依赖:外部:无；内部:无；本地:./BasePage。导出:WorkflowSharingModal。关键函数/方法:save、getModal、waitForModal、getUsersSelect、getVisibleDropdown、addUser、close。用于组装工作流页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/WorkflowSharingModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/WorkflowSharingModal.py

import { BasePage } from './BasePage';

export class WorkflowSharingModal extends BasePage {
	getModal() {
		return this.page.getByTestId('workflowShare-modal');
	}

	async waitForModal() {
		await this.getModal().waitFor({ state: 'visible', timeout: 5000 });
	}

	getUsersSelect() {
		return this.page.getByTestId('project-sharing-select').filter({ visible: true });
	}

	getVisibleDropdown() {
		return this.page.locator('.el-select-dropdown:visible');
	}

	async addUser(email: string) {
		await this.clickByTestId('project-sharing-select');
		await this.page
			.locator('.el-select-dropdown__item')
			.filter({ hasText: email.toLowerCase() })
			.click();
	}

	async save() {
		await this.clickByTestId('workflow-sharing-modal-save-button');
		await this.getModal().waitFor({ state: 'hidden' });
	}

	async close() {
		await this.getModal().locator('.el-dialog__close').first().click();
	}
}
