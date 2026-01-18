"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-constructor-in-backend-module.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoConstructorInBackendModuleRule。关键函数/方法:create。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-constructor-in-backend-module.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_constructor_in_backend_module.py

import { ESLintUtils, TSESTree } from '@typescript-eslint/utils';

export const NoConstructorInBackendModuleRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description:
				'A class decorated with `@BackendModule` must not have a constructor. This ensures that module dependencies are loaded only when the module is used.',
		},
		messages: {
			noConstructorInBackendModule:
				'Remove the constructor from the class decorated with `@BackendModule`.',
		},
		fixable: 'code',
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			'ClassDeclaration MethodDefinition[kind="constructor"]'(node: TSESTree.MethodDefinition) {
				const classDeclaration = node.parent?.parent as TSESTree.ClassDeclaration;

				const isBackendModule =
					classDeclaration.decorators?.some(
						(d) =>
							d.expression.type === 'CallExpression' &&
							d.expression.callee.type === 'Identifier' &&
							d.expression.callee.name === 'BackendModule',
					) ?? false;

				if (isBackendModule) {
					context.report({
						node,
						messageId: 'noConstructorInBackendModule',
						fix: (fixer) => fixer.remove(node),
					});
				}
			},
		};
	},
});
