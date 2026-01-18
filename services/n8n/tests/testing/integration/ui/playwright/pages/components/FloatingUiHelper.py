"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/FloatingUiHelper.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:FloatingUiHelper。关键函数/方法:getVisiblePoppers、getVisiblePopper、getVisiblePopoverMenuItem、getVisiblePopoverOption。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/FloatingUiHelper.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/FloatingUiHelper.py

import type { Locator, Page } from '@playwright/test';

type GetByRoleName = NonNullable<Parameters<Locator['getByRole']>[1]>['name'];
type GetByRoleOptionsWithoutName = Omit<Parameters<Locator['getByRole']>[1], 'name'>;

export class FloatingUiHelper {
	constructor(protected readonly page: Page) {}

	getVisiblePoppers() {
		// Match Reka UI popovers (data-side is unique to Reka UI positioned content)
		return this.page.locator('[data-state="open"][data-side]');
	}

	getVisiblePopper() {
		// Match both Element+ poppers (.el-popper:visible) and Reka UI poppers ([data-state="open"])
		return this.page.locator(
			'.el-popper:visible, [data-state="open"][role="dialog"], [data-state="open"][role="menu"]',
		);
	}

	getVisiblePopoverMenuItem(name?: GetByRoleName, options: GetByRoleOptionsWithoutName = {}) {
		return this.getVisiblePopper()
			.getByRole('menuitem', { name, ...options })
			.filter({ visible: true });
	}

	getVisiblePopoverOption(name?: GetByRoleName, options: GetByRoleOptionsWithoutName = {}) {
		return this.getVisiblePopper()
			.getByRole('option', { name, ...options })
			.filter({ visible: true });
	}
}
