"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-unneeded-backticks.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoUnneededBackticksRule。关键函数/方法:create、TemplateLiteral。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-unneeded-backticks.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_unneeded_backticks.py

import { ESLintUtils } from '@typescript-eslint/utils';

export const NoUnneededBackticksRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description:
				'Template literal backticks may only be used for string interpolation or multiline strings.',
		},
		messages: {
			noUnneededBackticks: 'Use single or double quotes, not backticks',
		},
		fixable: 'code',
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			TemplateLiteral(node) {
				if (node.expressions.length > 0) return;
				if (node.quasis.every((q) => q.loc.start.line !== q.loc.end.line)) return;

				node.quasis.forEach((q) => {
					const escaped = q.value.raw.replace(/(?<!\\)'/g, "\\'");

					context.report({
						messageId: 'noUnneededBackticks',
						node,
						fix: (fixer) => fixer.replaceText(q, `'${escaped}'`),
					});
				});
			},
		};
	},
});
