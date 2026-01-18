"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-useless-catch-throw.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoUselessCatchThrowRule。关键函数/方法:create、CatchClause、fix。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-useless-catch-throw.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_useless_catch_throw.py

import { ESLintUtils } from '@typescript-eslint/utils';

export const NoUselessCatchThrowRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description: 'Disallow `try-catch` blocks where the `catch` only contains a `throw error`.',
		},
		messages: {
			noUselessCatchThrow: 'Remove useless `catch` block.',
		},
		fixable: 'code',
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			CatchClause(node) {
				if (
					node.body.body.length === 1 &&
					node.body.body[0].type === 'ThrowStatement' &&
					node.body.body[0].argument.type === 'Identifier' &&
					node.param?.type === 'Identifier' &&
					node.body.body[0].argument.name === node.param.name
				) {
					context.report({
						node,
						messageId: 'noUselessCatchThrow',
						fix(fixer) {
							const tryStatement = node.parent;
							const tryBlock = tryStatement.block;
							const sourceCode = context.sourceCode;
							const tryBlockText = sourceCode.getText(tryBlock);
							const tryBlockTextWithoutBraces = tryBlockText.slice(1, -1).trim();
							const indentedTryBlockText = tryBlockTextWithoutBraces
								.split('\n')
								.map((line) => line.replace(/\t/, ''))
								.join('\n');
							return fixer.replaceText(tryStatement, indentedTryBlockText);
						},
					});
				}
			},
		};
	},
});
