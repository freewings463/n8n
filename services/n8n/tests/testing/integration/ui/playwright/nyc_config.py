"""
MIGRATION-META:
  source_path: packages/testing/playwright/nyc.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright 的配置。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/nyc.config.ts -> services/n8n/tests/testing/integration/ui/playwright/nyc_config.py

const config = {
	reporter: ['html'],
	reportDir: 'coverage',
	tempDir: '.nyc_output',
	include: [
		'../../../packages/frontend/editor-ui/src/**/*.{js,ts,vue}',
		'../../../packages/frontend/editor-ui/dist/**/*.{js,ts}',
	],
	exclude: [
		'**/*.test.{js,ts}',
		'**/*.spec.{js,ts}',
		'**/node_modules/**',
		'**/coverage/**',
		'**/.nyc_output/**',
	],
	sourceMap: true,
};

export = config;
