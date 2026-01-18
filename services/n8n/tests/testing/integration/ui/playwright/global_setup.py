"""
MIGRATION-META:
  source_path: packages/testing/playwright/global-setup.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright 的模块。导入/依赖:外部:@playwright/test；内部:无；本地:./services/api-helper、./utils/url-helper。导出:无。关键函数/方法:globalSetup。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/global-setup.ts -> services/n8n/tests/testing/integration/ui/playwright/global_setup.py

import { request } from '@playwright/test';

import { ApiHelpers } from './services/api-helper';
import { getBackendUrl } from './utils/url-helper';

async function globalSetup() {
	console.log('🚀 Starting global setup...');

	// Check if backend URL is set (N8N_BACKEND_URL or N8N_BASE_URL)
	const n8nBaseUrl = getBackendUrl();
	if (!n8nBaseUrl) {
		console.log('⚠️  N8N_BASE_URL environment variable is not set, skipping database reset');
		return;
	}

	const resetE2eDb = process.env.RESET_E2E_DB;
	if (resetE2eDb !== 'true') {
		console.log('⚠️  RESET_E2E_DB is not set to "true", skipping database reset');
		return;
	}

	console.log(`🔄 Resetting database for ${n8nBaseUrl}...`);
	// Quick hack till we find out a better health check for the database reset command!
	await new Promise((resolve) => setTimeout(resolve, 3000));
	// Create standalone API request context
	const requestContext = await request.newContext({
		baseURL: n8nBaseUrl,
	});

	try {
		const api = new ApiHelpers(requestContext);
		await api.resetDatabase();
		console.log('✅ Database reset completed successfully');
	} catch (error) {
		console.error('❌ Failed to reset database:', error);
		throw error; // This will fail the entire test suite if database reset fails
	} finally {
		await requestContext.dispose();
	}

	console.log('🏁 Global setup completed');
}

// eslint-disable-next-line import-x/no-default-export
export default globalSetup;
