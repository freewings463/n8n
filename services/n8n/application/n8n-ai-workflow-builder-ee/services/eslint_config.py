"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/eslint.config.mjs
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee 的工作流配置。导入/依赖:外部:eslint/config；内部:@n8n/eslint-config/node；本地:无。导出:无。关键函数/方法:globalIgnores。用于集中定义工作流配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/eslint.config.mjs -> services/n8n/application/n8n-ai-workflow-builder-ee/services/eslint_config.py

import { defineConfig, globalIgnores } from 'eslint/config';
import { nodeConfig } from '@n8n/eslint-config/node';

export default defineConfig(
	globalIgnores(['jest.config*.js', 'evaluations/programmatic/python/.venv/**']),
	nodeConfig,
	{
	rules: {
		'unicorn/filename-case': ['error', { case: 'kebabCase' }],
		complexity: 'error',
		'@typescript-eslint/require-await': 'warn',
		'@typescript-eslint/naming-convention': 'warn',
	},
}, {
	files: ['./src/test/**/*.ts', './**/*.test.ts'],
	rules: {
		'@typescript-eslint/no-unsafe-assignment': 'warn',
	},
});
