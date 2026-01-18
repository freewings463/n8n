"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/SaveChangesModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:SaveChangesModal。关键函数/方法:getModal、getCancelButton、getCloseButton、getSaveButton、clickCancel、clickClose、clickSave。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/SaveChangesModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/SaveChangesModal.py

import type { Locator } from '@playwright/test';

/**
 * Save Changes Modal component for handling unsaved changes dialogs.
 * Appears when navigating away from workflow with unsaved changes.
 */
export class SaveChangesModal {
	constructor(private root: Locator) {}

	getModal(): Locator {
		return this.root.filter({ hasText: 'Save changes before leaving?' });
	}

	getCancelButton(): Locator {
		return this.root.locator('.btn--cancel');
	}

	getCloseButton(): Locator {
		return this.root.locator('.el-message-box__headerbtn');
	}

	getSaveButton(): Locator {
		return this.root.getByRole('button', { name: 'Save' });
	}

	async clickCancel(): Promise<void> {
		await this.getCancelButton().click();
	}

	async clickClose(): Promise<void> {
		await this.getCloseButton().click();
	}

	async clickSave(): Promise<void> {
		await this.getSaveButton().click();
	}
}
