"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/vite.config.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/node-cli 的配置。导入/依赖:外部:vitest/config；内部:无；本地:无。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI package default -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/vite.config.ts -> services/n8n/presentation/n8n-node-cli/cli/vite_config.py

import { defineConfig } from 'vitest/config';

export default defineConfig({
	test: {
		globals: true,
		disableConsoleIntercept: true,
		setupFiles: ['src/test-utils/setup.ts'],
	},
});
