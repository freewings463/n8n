"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/WorkerViewPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:无；内部:无；本地:./BasePage。导出:WorkerViewPage。关键函数/方法:getWorkerCards、getWorkerCard、getWorkerViewLicensed、getWorkerViewUnlicensed、getWorkerMenuItem、visitWorkerView。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/WorkerViewPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/WorkerViewPage.py

import { BasePage } from './BasePage';

export class WorkerViewPage extends BasePage {
	getWorkerCards() {
		return this.page.getByTestId('worker-card');
	}

	getWorkerCard(workerId: string) {
		return this.getWorkerCards().filter({ hasText: workerId });
	}

	getWorkerViewLicensed() {
		return this.page.getByTestId('worker-view-licensed');
	}

	getWorkerViewUnlicensed() {
		return this.page.getByTestId('worker-view-unlicensed');
	}

	getWorkerMenuItem() {
		return this.page.getByTestId('menu-item').getByText('Workers', { exact: true });
	}

	async visitWorkerView() {
		await this.page.goto('/settings/workers');
	}
}
