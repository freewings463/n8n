"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-plugin-community-nodes/src/plugin.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-plugin-community-nodes/src 的模块。导入/依赖:外部:eslint；内部:无；本地:./rules/index.js。导出:rules、configs、n8nCommunityNodesPlugin。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-plugin-community-nodes/src/plugin.ts -> services/n8n/infrastructure/n8n-eslint-plugin-community-nodes/configuration/tooling/src/plugin.py

import type { ESLint, Linter } from 'eslint';

import pkg from '../package.json' with { type: 'json' };
import { rules } from './rules/index.js';

const plugin = {
	meta: {
		name: pkg.name,
		version: pkg.version,
		namespace: '@n8n/community-nodes',
	},
	// @ts-expect-error Rules type does not match for typescript-eslint and eslint
	rules: rules as ESLint.Plugin['rules'],
} satisfies ESLint.Plugin;

const configs = {
	recommended: {
		ignores: ['eslint.config.{js,mjs,ts,mts}'],
		plugins: {
			'@n8n/community-nodes': plugin,
		},
		rules: {
			'@n8n/community-nodes/no-restricted-globals': 'error',
			'@n8n/community-nodes/no-restricted-imports': 'error',
			'@n8n/community-nodes/credential-password-field': 'error',
			'@n8n/community-nodes/no-deprecated-workflow-functions': 'error',
			'@n8n/community-nodes/node-usable-as-tool': 'error',
			'@n8n/community-nodes/package-name-convention': 'error',
			'@n8n/community-nodes/credential-test-required': 'error',
			'@n8n/community-nodes/no-credential-reuse': 'error',
			'@n8n/community-nodes/icon-validation': 'error',
			'@n8n/community-nodes/resource-operation-pattern': 'warn',
			'@n8n/community-nodes/credential-documentation-url': 'error',
		},
	},
	recommendedWithoutN8nCloudSupport: {
		ignores: ['eslint.config.{js,mjs,ts,mts}'],
		plugins: {
			'@n8n/community-nodes': plugin,
		},
		rules: {
			'@n8n/community-nodes/credential-password-field': 'error',
			'@n8n/community-nodes/no-deprecated-workflow-functions': 'error',
			'@n8n/community-nodes/node-usable-as-tool': 'error',
			'@n8n/community-nodes/package-name-convention': 'error',
			'@n8n/community-nodes/credential-test-required': 'error',
			'@n8n/community-nodes/no-credential-reuse': 'error',
			'@n8n/community-nodes/icon-validation': 'error',
			'@n8n/community-nodes/credential-documentation-url': 'error',
			'@n8n/community-nodes/resource-operation-pattern': 'warn',
		},
	},
} satisfies Record<string, Linter.Config>;

const pluginWithConfigs = { ...plugin, configs } satisfies ESLint.Plugin;

const n8nCommunityNodesPlugin = pluginWithConfigs;
export default pluginWithConfigs;
export { rules, configs, n8nCommunityNodesPlugin };
