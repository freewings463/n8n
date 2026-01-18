"""
MIGRATION-META:
  source_path: packages/@n8n/vitest-config/node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/vitest-config 的模块。导入/依赖:外部:vitest/config、vitest/node；内部:无；本地:无。导出:createVitestConfig、vitestConfig。关键函数/方法:createVitestConfig。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/vitest-config/node.ts -> services/n8n/infrastructure/n8n-vitest-config/configuration/tooling/node.py

import { defineConfig } from 'vitest/config';
import type { InlineConfig } from 'vitest/node';

export const createVitestConfig = (options: InlineConfig = {}) => {
	const vitestConfig = defineConfig({
		test: {
			silent: true,
			globals: true,
			environment: 'node',
			...(process.env.COVERAGE_ENABLED === 'true'
				? {
						coverage: {
							enabled: true,
							provider: 'v8',
							reporter: process.env.CI === 'true' ? 'cobertura' : 'text-summary',
							all: true,
						},
					}
				: {}),
			...options,
		},
	});

	return vitestConfig;
};

export const vitestConfig = createVitestConfig();
