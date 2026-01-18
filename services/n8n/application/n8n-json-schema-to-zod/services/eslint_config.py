"""
MIGRATION-META:
  source_path: packages/@n8n/json-schema-to-zod/eslint.config.mjs
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/json-schema-to-zod 的配置。导入/依赖:外部:eslint/config；内部:@n8n/eslint-config/node；本地:无。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Pure schema->validator transformation library -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/json-schema-to-zod/eslint.config.mjs -> services/n8n/application/n8n-json-schema-to-zod/services/eslint_config.py

import { defineConfig } from 'eslint/config';
import { nodeConfig } from '@n8n/eslint-config/node';

export default defineConfig(
	nodeConfig,
	{
		rules: {
			'unicorn/filename-case': ['error', { case: 'kebabCase' }],
			'@typescript-eslint/no-duplicate-imports': 'off',
			'import-x/no-cycle': 'off',
			complexity: 'error',

			// TODO: Remove this
			'no-constant-condition': 'warn',
		},
	},
	{
		files: ['**/*.test.ts'],
		rules: {
			'@typescript-eslint/no-unused-expressions': 'warn',
			'@typescript-eslint/naming-convention': 'warn',
			'@typescript-eslint/no-unsafe-assignment': 'warn',
			'@typescript-eslint/ban-ts-comment': ['warn', { 'ts-ignore': true }],
		},
	},
);
