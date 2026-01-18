"""
MIGRATION-META:
  source_path: packages/@n8n/vitest-config/frontend.ts
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
# TODO-REFACTOR-DDD: packages/@n8n/vitest-config/frontend.ts -> services/n8n/infrastructure/n8n-vitest-config/configuration/tooling/frontend.py

import { defineConfig } from 'vitest/config';
import type { InlineConfig } from 'vitest/node';

export const createVitestConfig = (options: InlineConfig = {}) => {
	const vitestConfig = defineConfig({
		test: {
			silent: true,
			globals: true,
			environment: 'jsdom',
			setupFiles: ['./src/__tests__/setup.ts'],
			coverage: {
				enabled: false,
				all: false,
				provider: 'v8',
				reporter: ['text-summary', 'lcov', 'html-spa'],
			},
			css: {
				modules: {
					classNameStrategy: 'non-scoped',
				},
			},
			...options,
		},
	});

	if (process.env.COVERAGE_ENABLED === 'true' && vitestConfig.test?.coverage) {
		const { coverage } = vitestConfig.test;
		coverage.enabled = true;
		if (process.env.CI === 'true' && coverage.provider === 'v8') {
			coverage.all = true;
			coverage.reporter = ['cobertura'];
		}
	}

	return vitestConfig;
};

export const vitestConfig = createVitestConfig();
