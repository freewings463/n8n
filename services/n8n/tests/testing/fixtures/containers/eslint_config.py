"""
MIGRATION-META:
  source_path: packages/testing/containers/eslint.config.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers 的配置。导入/依赖:外部:eslint/config；内部:@n8n/eslint-config/base；本地:无。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/eslint.config.mjs -> services/n8n/tests/testing/fixtures/containers/eslint_config.py

import { defineConfig } from 'eslint/config';
import { baseConfig } from '@n8n/eslint-config/base';

export default defineConfig(baseConfig, {
	rules: {
		'@typescript-eslint/naming-convention': [
			'error',
			// Add exception for Docker Compose labels
			{
				selector: 'objectLiteralProperty',
				format: null, // Allow any format
				filter: {
					regex: '^com\\.docker\\.',
					match: true,
				},
			},
		],
	},
});
