"""
MIGRATION-META:
  source_path: packages/testing/playwright/utils/index-helper.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/utils 的工具。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:locatorByIndex。关键函数/方法:locatorByIndex。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/utils/index-helper.ts -> services/n8n/tests/testing/integration/ui/playwright/utils/index_helper.py

import type { Locator } from '@playwright/test';

/**
 * Returns a locator for a specific element by index, or the original locator if no index is provided.
 * Without an index, Playwright throws an error when multiple matching elements are found.
 * @see https://playwright.dev/docs/locators#strictness
 */
export function locatorByIndex(locator: Locator, index?: number) {
	return typeof index === 'number' ? locator.nth(index) : locator;
}
