"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-dynamic-import-template.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoDynamicImportTemplateRule。关键函数/方法:create。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-dynamic-import-template.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_dynamic_import_template.py

import { ESLintUtils, type TSESTree } from '@typescript-eslint/utils';

export const NoDynamicImportTemplateRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description:
				'Disallow non-relative imports in template string argument to `await import()`, because `tsc-alias` as of 1.8.7 is unable to resolve aliased paths in this scenario.',
		},
		schema: [],
		messages: {
			noDynamicImportTemplate:
				'Use relative imports in template string argument to `await import()`, because `tsc-alias` as of 1.8.7 is unable to resolve aliased paths in this scenario.',
		},
	},
	defaultOptions: [],
	create(context) {
		return {
			'AwaitExpression > ImportExpression TemplateLiteral'(node: TSESTree.TemplateLiteral) {
				const templateValue = node.quasis[0].value.cooked;

				if (!templateValue?.startsWith('@/')) return;

				context.report({
					node,
					messageId: 'noDynamicImportTemplate',
				});
			},
		};
	},
});
