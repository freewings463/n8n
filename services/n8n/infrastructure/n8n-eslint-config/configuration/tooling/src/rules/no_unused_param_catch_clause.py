"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-unused-param-catch-clause.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoUnusedParamInCatchClauseRule。关键函数/方法:create、CatchClause。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-unused-param-catch-clause.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_unused_param_catch_clause.py

import { ESLintUtils } from '@typescript-eslint/utils';

export const NoUnusedParamInCatchClauseRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description: 'Unused param in catch clause must be omitted.',
		},
		messages: {
			removeUnusedParam: 'Remove unused param in catch clause',
		},
		fixable: 'code',
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			CatchClause(node) {
				if (node.param?.type === 'Identifier' && node.param.name.startsWith('_')) {
					const start = node.range[0] + 'catch '.length;
					const end = node.param.range[1] + '()'.length;

					context.report({
						messageId: 'removeUnusedParam',
						node,
						fix: (fixer) => fixer.removeRange([start, end]),
					});
				}
			},
		};
	},
});
