"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-top-level-relative-imports-in-backend-module.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:./path。导出:NoTopLevelRelativeImportsInBackendModuleRule。关键函数/方法:create。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-top-level-relative-imports-in-backend-module.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_top_level_relative_imports_in_backend_module.py

import { ESLintUtils, TSESTree } from '@typescript-eslint/utils';

export const NoTopLevelRelativeImportsInBackendModuleRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description:
				'Relative imports in `.module.ts` files must be placed inside the `init` method. This ensures that module imports are loaded only when the module is used.',
		},
		messages: {
			placeInsideInit:
				"Place this relative import inside the `init` method, using `await import('./path')` syntax.",
		},
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			'Program > ImportDeclaration'(node: TSESTree.ImportDeclaration) {
				if (node.source.value.startsWith('.')) {
					context.report({ node, messageId: 'placeInsideInit' });
				}
			},
		};
	},
});
