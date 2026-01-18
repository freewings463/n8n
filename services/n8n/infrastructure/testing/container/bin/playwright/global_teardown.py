"""
MIGRATION-META:
  source_path: packages/testing/playwright/global-teardown.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:globalTeardown、execSync。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected child_process execution -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/global-teardown.ts -> services/n8n/infrastructure/testing/container/bin/playwright/global_teardown.py

import { execSync } from 'child_process';

function globalTeardown() {
	console.log('🧹 Starting global teardown...');

	const ports = [5678, 8080];

	for (const port of ports) {
		try {
			// Find process ID using the port
			const pid = execSync(`lsof -ti :${port}`, { encoding: 'utf-8' }).trim();

			if (pid) {
				console.log(`- Killing process ${pid} on port ${port}`);
				execSync(`kill -9 ${pid}`);
			}
		} catch (error) {
			// lsof returns non-zero exit code if no process is found
			console.log(`- No process found on port ${port}`);
		}
	}

	console.log('🏁 Global teardown completed');
}

// eslint-disable-next-line import-x/no-default-export
export default globalTeardown;
