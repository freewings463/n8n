"""
MIGRATION-META:
  source_path: packages/testing/playwright/composables/DataTablesComposer.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/composables 的组合式函数。导入/依赖:外部:无；内部:无；本地:../pages/n8nPage。导出:DataTableComposer。关键函数/方法:createNewDataTable、createDataTableInNewProject。用于封装该模块复用逻辑（hooks/composables）供组件组合。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/composables/DataTablesComposer.ts -> services/n8n/tests/testing/integration/ui/playwright/composables/DataTablesComposer.py

import type { n8nPage } from '../pages/n8nPage';

export class DataTableComposer {
	constructor(private readonly n8n: n8nPage) {}

	async createNewDataTable(name: string) {
		const nameInput = this.n8n.dataTable.getNewDataTableNameInput();
		await nameInput.fill(name);
		await this.n8n.dataTable.getFromScratchOption().click();
		await this.n8n.dataTable.getProceedFromSelectButton().click();
	}

	/**
	 * Creates project and data table inside it, navigating to project 'Data Table' tab
	 * @param projectName
	 * @param dataTableName
	 * @param source - from where the creation is initiated (empty state or header dropdown)
	 */
	async createDataTableInNewProject(
		projectName: string,
		dataTableName: string,
		source: 'empty-state' | 'header-dropdown',
		fromDataTableTab: boolean = true,
	) {
		await this.n8n.projectComposer.createProject(projectName);
		const { projectId } = await this.n8n.projectComposer.createProject();

		if (fromDataTableTab) {
			await this.n8n.page.goto(`projects/${projectId}/datatables`);
		} else {
			await this.n8n.page.goto(`projects/${projectId}`);
		}

		if (source === 'empty-state') {
			await this.n8n.dataTable.clickEmptyStateButton();
		} else {
			await this.n8n.dataTable.clickAddDataTableAction(fromDataTableTab);
		}
		await this.n8n.dataTableComposer.createNewDataTable(dataTableName);
		await this.n8n.page.goto(`projects/${projectId}/datatables`);
	}
}
