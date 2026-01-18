"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/eslint.config.mjs
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions 的配置。导入/依赖:外部:eslint/config；内部:@n8n/eslint-config/base；本地:无。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/eslint.config.mjs -> services/n8n/domain/n8n-permissions/policies/eslint_config.py

import { defineConfig } from 'eslint/config';
import { baseConfig } from '@n8n/eslint-config/base';

export default defineConfig(baseConfig, {
	rules: {
		'unicorn/filename-case': ['error', { case: 'kebabCase' }],

		// TODO: Remove this
		'import-x/order': 'warn',
		'@typescript-eslint/naming-convention': 'warn',
	},
});
