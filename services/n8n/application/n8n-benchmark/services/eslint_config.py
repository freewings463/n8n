"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/eslint.config.mjs
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/benchmark 的配置。导入/依赖:外部:eslint/config；内部:@n8n/eslint-config/node；本地:无。导出:无。关键函数/方法:globalIgnores。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Benchmark orchestration logic -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/eslint.config.mjs -> services/n8n/application/n8n-benchmark/services/eslint_config.py

import { defineConfig, globalIgnores } from 'eslint/config';
import { nodeConfig } from '@n8n/eslint-config/node';

export default defineConfig(
	nodeConfig,
	globalIgnores(['scenarios/**', 'scripts/**']),
	{
		rules: {
			'unicorn/filename-case': ['error', { case: 'kebabCase' }],
			'n8n-local-rules/no-plain-errors': 'off',
			complexity: 'error',
			'@typescript-eslint/naming-convention': 'warn',
			'no-empty': 'warn',
		},
	},
	{
		files: ['./src/commands/*.ts'],
		rules: {
			'import-x/no-default-export': 'off',
		},
	},
);
