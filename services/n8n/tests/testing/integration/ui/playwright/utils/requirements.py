"""
MIGRATION-META:
  source_path: packages/testing/playwright/utils/requirements.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/utils 的工具。导入/依赖:外部:@playwright/test；内部:无；本地:../config/intercepts、../pages/n8nPage、../Types。导出:无。关键函数/方法:setupTestRequirements、setContextSettings。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/utils/requirements.ts -> services/n8n/tests/testing/integration/ui/playwright/utils/requirements.py

import type { BrowserContext } from '@playwright/test';

import { setContextSettings } from '../config/intercepts';
import type { n8nPage } from '../pages/n8nPage';
import { TestError, type TestRequirements } from '../Types';

export async function setupTestRequirements(
	n8n: n8nPage,
	context: BrowserContext,
	requirements: TestRequirements,
): Promise<void> {
	// 0. Setup browser storage before creating a new page
	if (requirements.storage) {
		await context.addInitScript((storage) => {
			// Set localStorage items
			for (const [key, value] of Object.entries(storage)) {
				window.localStorage.setItem(key, value);
			}
		}, requirements.storage);
	}

	// 1. Setup frontend settings override
	if (requirements.config?.settings) {
		// Store settings for this context
		setContextSettings(context, requirements.config.settings);
	}

	// 2. Setup feature flags
	if (requirements.config?.features) {
		for (const [feature, enabled] of Object.entries(requirements.config.features)) {
			if (enabled) {
				await n8n.api.enableFeature(feature);
			} else {
				await n8n.api.disableFeature(feature);
			}
		}
	}

	// 3. Setup API intercepts
	if (requirements.intercepts) {
		for (const config of Object.values(requirements.intercepts)) {
			await n8n.page.route(config.url, async (route) => {
				await route.fulfill({
					status: config.status ?? 200,
					contentType: config.contentType ?? 'application/json',
					body:
						typeof config.response === 'string' ? config.response : JSON.stringify(config.response),
				});
			});
		}
	}

	// 4. Setup workflows
	if (requirements.workflow) {
		const entries =
			typeof requirements.workflow === 'string'
				? [[requirements.workflow, requirements.workflow]]
				: Object.entries(requirements.workflow);

		for (const [name, workflowData] of entries) {
			try {
				// Import workflow using the n8n page object
				await n8n.navigate.toWorkflow('new');
				await n8n.canvas.importWorkflow(name, workflowData);
			} catch (error) {
				throw new TestError(`Failed to create workflow ${name}: ${String(error)}`);
			}
		}
	}
}
