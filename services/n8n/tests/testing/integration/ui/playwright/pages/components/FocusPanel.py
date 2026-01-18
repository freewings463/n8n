"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/FocusPanel.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:FocusPanel。关键函数/方法:getHeaderNodeName、getParameterInputField、getMapper。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/FocusPanel.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/FocusPanel.py

import type { Locator } from '@playwright/test';

export class FocusPanel {
	constructor(private root: Locator) {}

	/**
	 * Accessors
	 */

	getHeaderNodeName(): Locator {
		return this.root.locator('header').getByTestId('inline-edit-preview');
	}

	getParameterInputField(path: string): Locator {
		return this.root.locator(
			`[data-test-id="parameter-input-field"][title="Parameter: \\"${path}\\""]`,
		);
	}

	getMapper(): Locator {
		// find from the entire page because the mapper is rendered as portal
		return this.root.page().getByRole('dialog').getByTestId('ndv-input-panel');
	}
}
