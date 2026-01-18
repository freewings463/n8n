"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-interpolation-in-regular-string.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoInterpolationInRegularStringRule。关键函数/方法:create、Literal。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-interpolation-in-regular-string.ts -> services/n8n/tests/n8n-eslint-config/unit/rules/no_interpolation_in_regular_string.py

import { ESLintUtils } from '@typescript-eslint/utils';

export const NoInterpolationInRegularStringRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description: 'String interpolation `${...}` requires backticks, not single or double quotes.',
		},
		messages: {
			useBackticks: 'Use backticks to interpolate',
		},
		fixable: 'code',
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			Literal(node) {
				if (typeof node.value !== 'string') return;

				if (/\$\{/.test(node.value)) {
					context.report({
						messageId: 'useBackticks',
						node,
						fix: (fixer) => fixer.replaceText(node, `\`${node.value}\``),
					});
				}
			},
		};
	},
});
