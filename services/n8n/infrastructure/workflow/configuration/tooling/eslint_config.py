"""
MIGRATION-META:
  source_path: packages/workflow/eslint.config.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/workflow 的工作流配置。导入/依赖:外部:eslint/config；内部:@n8n/eslint-config/base；本地:无。导出:无。关键函数/方法:无。用于集中定义工作流配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow tooling/config file
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/eslint.config.mjs -> services/n8n/infrastructure/workflow/configuration/tooling/eslint_config.py

import { defineConfig } from 'eslint/config';
import { baseConfig } from '@n8n/eslint-config/base';

export default defineConfig(
	baseConfig,
	{
		rules: {
			'unicorn/filename-case': ['error', { case: 'kebabCase' }],
			complexity: ['error', 23],

			// TODO: remove these
			'no-empty': 'warn',
			'id-denylist': 'warn',
			'no-fallthrough': 'warn',
			'no-useless-escape': 'warn',
			'import-x/order': 'warn',
			'no-extra-boolean-cast': 'warn',
			'no-case-declarations': 'warn',
			'no-prototype-builtins': 'warn',
			'@typescript-eslint/naming-convention': 'warn',
			'@typescript-eslint/no-base-to-string': 'warn',
			'@typescript-eslint/no-redundant-type-constituents': 'warn',
			'@typescript-eslint/prefer-nullish-coalescing': 'warn',
			'@typescript-eslint/prefer-optional-chain': 'warn',
			'@typescript-eslint/return-await': ['error', 'always'],
			'@typescript-eslint/no-empty-object-type': 'warn',
			'@typescript-eslint/no-unsafe-function-type': 'warn',
			'@typescript-eslint/no-duplicate-type-constituents': 'warn',
			'@typescript-eslint/no-unsafe-call': 'warn',
		},
	},
	{
		files: ['**/*.test.ts'],
		rules: {
			// TODO: remove these
			'prefer-const': 'warn',
			'@typescript-eslint/no-unused-expressions': 'warn',
			'@typescript-eslint/no-explicit-any': 'warn',
			'@typescript-eslint/no-unsafe-member-access': 'warn',
			'@typescript-eslint/no-unsafe-assignment': 'warn',
			'@typescript-eslint/no-unsafe-return': 'warn',
			'@typescript-eslint/ban-ts-comment': ['warn', { 'ts-ignore': true }],
		},
	},
);
