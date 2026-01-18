"""
MIGRATION-META:
  source_path: packages/extensions/insights/tsdown.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/extensions/insights 的Insights配置。导入/依赖:外部:tsdown；内部:无；本地:无。导出:无。关键函数/方法:无。用于集中定义Insights配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Extensions package -> infrastructure/configuration/tooling/extensions
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/extensions/insights/tsdown.config.ts -> services/n8n/infrastructure/extensions/configuration/tooling/extensions/insights/tsdown_config.py

import { defineConfig } from 'tsdown';

export default defineConfig({
	entry: [
		'src/backend/**/*.ts',
		'!src/backend/**/*.test.ts',
		'!src/backend/**/*.d.ts',
		'!src/backend/__tests__**/*',
	],
	outDir: 'dist/backend',
	format: ['cjs', 'esm'],
	dts: true,
	sourcemap: true,
	tsconfig: 'tsconfig.backend.json',
	hash: false,
});
