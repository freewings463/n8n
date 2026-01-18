"""
MIGRATION-META:
  source_path: packages/extensions/insights/eslint.config.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/extensions/insights 的Insights配置。导入/依赖:外部:eslint/config；内部:@n8n/eslint-config/base；本地:无。导出:无。关键函数/方法:globalIgnores。用于集中定义Insights配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Extensions package -> infrastructure/configuration/tooling/extensions
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/extensions/insights/eslint.config.mjs -> services/n8n/infrastructure/extensions/configuration/tooling/extensions/insights/eslint_config.py

import { defineConfig, globalIgnores } from 'eslint/config';
import { baseConfig } from '@n8n/eslint-config/base';

export default defineConfig(
	baseConfig,
	globalIgnores(['src/shims.d.ts']),
	{
		rules: {
			'unicorn/filename-case': ['error', { case: 'kebabCase' }],

			// TODO: Remove these
			'import-x/order': 'warn',
			'import-x/no-default-export': 'warn',
			'@typescript-eslint/no-unsafe-argument': 'warn',
			'@typescript-eslint/no-unsafe-call': 'warn',
			'@typescript-eslint/no-unsafe-member-access': 'warn',
		},
	},
	{
		files: ['src/backend/**/*.ts'],
		languageOptions: {
			parserOptions: {
				project: ['./tsconfig.backend.json'],
			},
		},
	},
	{
		files: ['src/frontend/**/*.ts'],
		languageOptions: {
			parserOptions: {
				project: ['./tsconfig.frontend.json'],
			},
		},
	},
);
