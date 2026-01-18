"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-skipped-tests.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoSkippedTestsRule。关键函数/方法:create、toMessageId、MemberExpression、CallExpression。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-skipped-tests.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_skipped_tests.py

import { ESLintUtils } from '@typescript-eslint/utils';

export const NoSkippedTestsRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description: 'Tests must not be skipped.',
		},
		messages: {
			removeSkip: 'Remove `.skip()` call',
			removeOnly: 'Remove `.only()` call',
			removeXPrefix: 'Remove `x` prefix',
		},
		fixable: 'code',
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		const TESTING_FUNCTIONS = new Set(['test', 'it', 'describe']);
		const SKIPPING_METHODS = new Set(['skip', 'only']);
		const PREFIXED_TESTING_FUNCTIONS = new Set(['xtest', 'xit', 'xdescribe']);
		const toMessageId = (s: string) =>
			('remove' + s.charAt(0).toUpperCase() + s.slice(1)) as
				| 'removeSkip'
				| 'removeOnly'
				| 'removeXPrefix';

		return {
			MemberExpression(node) {
				if (
					node.object.type === 'Identifier' &&
					TESTING_FUNCTIONS.has(node.object.name) &&
					node.property.type === 'Identifier' &&
					SKIPPING_METHODS.has(node.property.name)
				) {
					context.report({
						messageId: toMessageId(node.property.name),
						node,
						fix: (fixer) => {
							const [start, end] = node.property.range;
							return fixer.removeRange([start - '.'.length, end]);
						},
					});
				}
			},
			CallExpression(node) {
				if (node.callee.type === 'Identifier' && PREFIXED_TESTING_FUNCTIONS.has(node.callee.name)) {
					context.report({
						messageId: 'removeXPrefix',
						node,
						fix: (fixer) => fixer.replaceText(node.callee, 'test'),
					});
				}
			},
		};
	},
});
