"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-plain-errors.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoPlainErrorsRule。关键函数/方法:create、ThrowStatement。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-plain-errors.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_plain_errors.py

import { ESLintUtils, TSESTree } from '@typescript-eslint/utils';

export const NoPlainErrorsRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description:
				'Only `ApplicationError` (from the `workflow` package) or its child classes must be thrown. This ensures the error will be normalized when reported to Sentry, if applicable.',
		},
		messages: {
			useApplicationError:
				'Throw an `ApplicationError` (from the `workflow` package) or its child classes.',
		},
		fixable: 'code',
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			ThrowStatement(node) {
				if (!node.argument) return;

				const isNewError =
					node.argument.type === TSESTree.AST_NODE_TYPES.NewExpression &&
					node.argument.callee.type === TSESTree.AST_NODE_TYPES.Identifier &&
					node.argument.callee.name === 'Error';

				const isNewlessError =
					node.argument.type === TSESTree.AST_NODE_TYPES.CallExpression &&
					node.argument.callee.type === TSESTree.AST_NODE_TYPES.Identifier &&
					node.argument.callee.name === 'Error';

				if (isNewError || isNewlessError) {
					return context.report({
						messageId: 'useApplicationError',
						node,
						fix: (fixer) =>
							fixer.replaceText(
								node,
								`throw new ApplicationError(${(node.argument as TSESTree.CallExpression).arguments
									.map((arg) => context.sourceCode.getText(arg))
									.join(', ')})`,
							),
					});
				}
			},
		};
	},
});
