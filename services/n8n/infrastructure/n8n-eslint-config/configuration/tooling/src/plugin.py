"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/plugin.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src 的模块。导入/依赖:外部:eslint；内部:无；本地:./rules/index.js。导出:localRulesPlugin。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/plugin.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/plugin.py

import type { ESLint } from 'eslint';
import { rules } from './rules/index.js';

const plugin = {
	meta: {
		name: 'n8n-local-rules',
	},
	configs: {},
	// @ts-expect-error Rules type does not match for typescript-eslint and eslint
	rules: rules as ESLint.Plugin['rules'],
} satisfies ESLint.Plugin;

export const localRulesPlugin = {
	...plugin,
	configs: {
		recommended: {
			plugins: {
				'n8n-local-rules': plugin,
			},
			rules: {
				'n8n-local-rules/no-uncaught-json-parse': 'error',
				'n8n-local-rules/no-json-parse-json-stringify': 'error',
				'n8n-local-rules/no-unneeded-backticks': 'error',
				'n8n-local-rules/no-interpolation-in-regular-string': 'error',
				'n8n-local-rules/no-unused-param-in-catch-clause': 'error',
				'n8n-local-rules/no-useless-catch-throw': 'error',
				'n8n-local-rules/no-internal-package-import': 'error',
				'n8n-local-rules/no-type-only-import-in-di': 'error',
			},
		},
	},
} satisfies ESLint.Plugin;
