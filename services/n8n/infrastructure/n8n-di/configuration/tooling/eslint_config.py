"""
MIGRATION-META:
  source_path: packages/@n8n/di/eslint.config.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/di 的配置。导入/依赖:外部:eslint/config；内部:@n8n/eslint-config/base；本地:无。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package root tooling/config file
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/di/eslint.config.mjs -> services/n8n/infrastructure/n8n-di/configuration/tooling/eslint_config.py

import { defineConfig } from 'eslint/config';
import { baseConfig } from '@n8n/eslint-config/base';

export default defineConfig(baseConfig, {
	rules: {
		'unicorn/filename-case': ['error', { case: 'kebabCase' }],

		// TODO: Remove this
		'@typescript-eslint/naming-convention': 'warn',
		'@typescript-eslint/no-unsafe-function-type': 'warn',
		'import-x/order': 'warn',
	},
});
