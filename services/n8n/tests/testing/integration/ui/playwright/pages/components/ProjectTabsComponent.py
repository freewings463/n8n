"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/ProjectTabsComponent.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:ProjectTabsComponent。关键函数/方法:clickCredentialsTab、clickWorkflowsTab、clickDataTablesTab、clickVariablesTab。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/ProjectTabsComponent.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/ProjectTabsComponent.py

import type { Page } from '@playwright/test';

/**
 * ProjectTabs component - navigation tabs within a project view
 * Mirrors the ProjectTabs.vue component in the frontend
 */
export class ProjectTabsComponent {
	constructor(private readonly page: Page) {}

	async clickCredentialsTab() {
		await this.page
			.getByTestId('project-tabs')
			.getByRole('link', { name: /credentials/i })
			.click();
	}

	async clickWorkflowsTab() {
		await this.page
			.getByTestId('project-tabs')
			.getByRole('link', { name: /workflows/i })
			.click();
	}

	async clickDataTablesTab() {
		await this.page
			.getByTestId('project-tabs')
			.getByRole('link', { name: /data tables/i })
			.click();
	}

	async clickVariablesTab() {
		await this.page
			.getByTestId('project-tabs')
			.getByRole('link', { name: /variables/i })
			.click();
	}
}
