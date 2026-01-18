"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-plugin-community-nodes/eslint.config.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-plugin-community-nodes 的配置。导入/依赖:外部:eslint/config、eslint-plugin-eslint-plugin；内部:@n8n/eslint-config/node；本地:无。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-plugin-community-nodes/eslint.config.mjs -> services/n8n/infrastructure/n8n-eslint-plugin-community-nodes/configuration/tooling/eslint_config.py

import { defineConfig } from 'eslint/config';
import { nodeConfig } from '@n8n/eslint-config/node';
import eslintPlugin from 'eslint-plugin-eslint-plugin';

export default defineConfig([
	nodeConfig,
	eslintPlugin.configs.recommended,
	{
		files: ['src/**/*.ts'],
		languageOptions: {
			parserOptions: {
				project: './tsconfig.json',
				allowDefaultProject: true,
			},
		},
		rules: {
			// We use RuleCreator which adds this automatically
			'eslint-plugin/require-meta-docs-url': 'off',
			// typescript-eslint uses different pattern
			'eslint-plugin/require-meta-default-options': 'off',
			// Disable naming convention for plugin configs (ESLint rule names use kebab-case)
			'@typescript-eslint/naming-convention': 'off',
			// Allow default exports for ESLint plugin
			'import-x/no-default-export': 'off',
		},
	},
]);
