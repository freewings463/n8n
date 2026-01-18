"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/BecomeCreatorCTAPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:无；内部:无；本地:./BasePage。导出:BecomeCreatorCTAPage。关键函数/方法:getBecomeTemplateCreatorCta、getCloseBecomeTemplateCreatorCtaButton、closeBecomeTemplateCreatorCta。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/BecomeCreatorCTAPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/BecomeCreatorCTAPage.py

import { BasePage } from './BasePage';

export class BecomeCreatorCTAPage extends BasePage {
	getBecomeTemplateCreatorCta() {
		return this.page.getByTestId('become-template-creator-cta');
	}

	getCloseBecomeTemplateCreatorCtaButton() {
		return this.page.getByTestId('close-become-template-creator-cta');
	}

	async closeBecomeTemplateCreatorCta() {
		await this.getCloseBecomeTemplateCreatorCtaButton().click();
	}
}
