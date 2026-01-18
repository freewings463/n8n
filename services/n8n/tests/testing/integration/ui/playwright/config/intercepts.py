"""
MIGRATION-META:
  source_path: packages/testing/playwright/config/intercepts.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/config 的配置。导入/依赖:外部:@playwright/test、lodash/cloneDeep、lodash/merge；内部:无；本地:无。导出:setContextSettings、getContextSettings。关键函数/方法:setContextSettings、getContextSettings、setupDefaultInterceptors、async。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/config/intercepts.ts -> services/n8n/tests/testing/integration/ui/playwright/config/intercepts.py

import type { BrowserContext, Route } from '@playwright/test';
import cloneDeep from 'lodash/cloneDeep';
import merge from 'lodash/merge';

const contextSettings = new Map<BrowserContext, Partial<Record<string, unknown>>>();

export function setContextSettings(
	context: BrowserContext,
	settings: Partial<Record<string, unknown>>,
) {
	contextSettings.set(context, settings);
}

export function getContextSettings(context: BrowserContext) {
	return contextSettings.get(context);
}

export async function setupDefaultInterceptors(target: BrowserContext) {
	// Global /rest/settings intercept - always active like Cypress
	// TODO: Remove this as a global and move it per test
	await target.route('**/rest/settings', async (route: Route) => {
		try {
			const originalResponse = await route.fetch();
			const originalJson = await originalResponse.json();

			// Get settings stored for this specific context
			const testSettings = getContextSettings(target);

			// Deep merge test settings with backend settings (like Cypress)
			const modifiedData = {
				data:
					testSettings && Object.keys(testSettings).length > 0
						? merge(cloneDeep(originalJson.data), testSettings)
						: originalJson.data,
			};

			await route.fulfill({
				status: originalResponse.status(),
				headers: originalResponse.headers(),
				contentType: 'application/json',
				body: JSON.stringify(modifiedData),
			});
		} catch (error) {
			console.error('Error in /rest/settings intercept:', error);
			await route.continue();
		}
	});

	// POST /rest/credentials/test
	await target.route('**/rest/credentials/test', async (route: Route) => {
		if (route.request().method() === 'POST') {
			await route.fulfill({
				contentType: 'application/json',
				body: JSON.stringify({ data: { status: 'success', message: 'Tested successfully' } }),
			});
		} else {
			await route.continue();
		}
	});

	// POST /rest/license/renew
	await target.route('**/rest/license/renew', async (route: Route) => {
		if (route.request().method() === 'POST') {
			await route.fulfill({
				contentType: 'application/json',
				body: JSON.stringify({
					data: {
						usage: { activeWorkflowTriggers: { limit: -1, value: 0, warningThreshold: 0.8 } },
						license: { planId: '', planName: 'Community' },
					},
				}),
			});
		} else {
			await route.continue();
		}
	});

	// Pathname /api/health
	await target.route(
		(url) => url.pathname.endsWith('/api/health'),
		async (route: Route) => {
			await route.fulfill({
				contentType: 'application/json',
				body: JSON.stringify({ status: 'OK' }),
			});
		},
	);

	// Pathname /api/versions/*
	await target.route(
		(url) => url.pathname.startsWith('/api/versions/'),
		async (route: Route) => {
			await route.fulfill({
				contentType: 'application/json',
				body: JSON.stringify([
					{
						name: '1.45.1',
						createdAt: '2023-08-18T11:53:12.857Z',
						hasSecurityIssue: null,
						hasSecurityFix: null,
						securityIssueFixVersion: null,
						hasBreakingChange: null,
						documentationUrl: 'https://docs.n8n.io/release-notes/#n8n131',
						nodes: [],
						description: 'Includes <strong>bug fixes</strong>',
					},
					{
						name: '1.0.5',
						createdAt: '2023-07-24T10:54:56.097Z',
						hasSecurityIssue: false,
						hasSecurityFix: null,
						securityIssueFixVersion: null,
						hasBreakingChange: true,
						documentationUrl: 'https://docs.n8n.io/release-notes/#n8n104',
						nodes: [],
						description:
							'Includes <strong>core functionality</strong> and <strong>bug fixes</strong>',
					},
				]),
			});
		},
	);
}
