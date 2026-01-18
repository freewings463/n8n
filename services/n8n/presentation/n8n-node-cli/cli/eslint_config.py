"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/eslint.config.mjs
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/node-cli 的配置。导入/依赖:外部:eslint/config；内部:@n8n/eslint-config/node；本地:无。导出:无。关键函数/方法:globalIgnores。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI package default -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/eslint.config.mjs -> services/n8n/presentation/n8n-node-cli/cli/eslint_config.py

import { defineConfig, globalIgnores } from 'eslint/config';
import { nodeConfig } from '@n8n/eslint-config/node';

export default defineConfig(
	globalIgnores(['src/template/templates/**/template', 'src/template/templates/shared']),
	nodeConfig,
	{
		files: ['**/*.test.ts', 'src/test-utils/**/*'],
		rules: {
			'import-x/no-extraneous-dependencies': ['error', { devDependencies: true }],
		},
	},
	{
		files: ['src/commands/**/*.ts', 'src/modules.d.ts', 'src/configs/eslint.ts'],
		rules: { 'import-x/no-default-export': 'off', '@typescript-eslint/naming-convention': 'off' },
	},
);
