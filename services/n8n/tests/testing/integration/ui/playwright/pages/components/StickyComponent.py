"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/StickyComponent.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:../BasePage。导出:StickyComponent。关键函数/方法:getAddButton、getStickies、getStickyByIndex、addSticky、addFromContextMenu、getDefaultStickyGuideLink。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/StickyComponent.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/StickyComponent.py

import type { Locator, Page } from '@playwright/test';

import { BasePage } from '../BasePage';

/**
 * Sticky note component for canvas interactions.
 * Used within CanvasPage as `n8n.canvas.sticky.*`
 *
 * @example
 * // Access via canvas page
 * await n8n.canvas.sticky.addSticky();
 * await expect(n8n.canvas.sticky.getStickies()).toHaveCount(1);
 */
export class StickyComponent extends BasePage {
	constructor(page: Page) {
		super(page);
	}

	getAddButton(): Locator {
		return this.page.getByTestId('add-sticky-button');
	}

	getStickies(): Locator {
		return this.page.getByTestId('sticky');
	}

	getStickyByIndex(index: number): Locator {
		return this.getStickies().nth(index);
	}

	async addSticky(): Promise<void> {
		await this.getAddButton().click();
	}

	/**
	 * Add a sticky from the context menu, targets top left corner of canvas, so could fail if it's covered
	 * @param canvasPane - The canvas pane locator
	 */
	async addFromContextMenu(canvasPane: Locator): Promise<void> {
		await canvasPane.click({
			button: 'right',
			position: { x: 10, y: 10 },
		});
		await this.page.getByText('Add sticky note').click();
	}

	getDefaultStickyGuideLink(): Locator {
		return this.getStickies().first().getByRole('link', { name: 'Guide' });
	}
}
