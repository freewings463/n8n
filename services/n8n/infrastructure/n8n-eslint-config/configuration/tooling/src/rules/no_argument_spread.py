"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-argument-spread.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoArgumentSpreadRule。关键函数/方法:create、CallExpression、NewExpression。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-argument-spread.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_argument_spread.py

import { ESLintUtils } from '@typescript-eslint/utils';

export const NoArgumentSpreadRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description:
				'Avoid spreading potentially large arrays in function or constructor calls — can cause stack overflows. Use `.apply` or `Reflect.construct` instead.',
		},
		fixable: 'code',
		messages: {
			noUnboundedSpread:
				'Avoid spreading an array in function or constructor calls unless known to be small.',
			replaceWithApply:
				'Replace `array.push(...largeArray)` with `array.push.apply(array, largeArray)` to avoid potential stack overflows.',
			replaceWithReflect:
				'Replace `new Constructor(...args)` with `Reflect.construct(Constructor, args)` to avoid potential stack overflows.',
		},
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			CallExpression(node) {
				for (const arg of node.arguments) {
					if (arg.type !== 'SpreadElement') continue;

					const spreadArg = arg.argument;

					// Allow spread of inline arrays
					if (spreadArg.type === 'ArrayExpression') return;

					// Only autofix if it's the sole argument
					const canFix = node.arguments.length === 1;

					context.report({
						node,
						messageId: 'replaceWithApply',
						fix: canFix
							? (fixer) => {
									const source = context.sourceCode;

									if (node.callee.type === 'MemberExpression') {
										// Preserve `this`
										const thisText = source.getText(node.callee.object);
										const calleeText = source.getText(node.callee);
										const argText = source.getText(spreadArg);
										return fixer.replaceText(node, `${calleeText}.apply(${thisText}, ${argText})`);
									} else {
										// Not a memberexpression, use undefined as thisArg
										const calleeText = source.getText(node.callee);
										const argText = source.getText(spreadArg);
										return fixer.replaceText(node, `${calleeText}.apply(undefined, ${argText})`);
									}
								}
							: null,
					});
				}
			},

			NewExpression(node) {
				for (const arg of node.arguments || []) {
					if (arg.type !== 'SpreadElement') continue;

					const spreadArg = arg.argument;

					if (spreadArg.type === 'ArrayExpression') return;

					const canFix = node.arguments.length === 1;

					context.report({
						node,
						messageId: 'replaceWithReflect',
						fix: canFix
							? (fixer) => {
									const source = context.sourceCode;
									const ctorText = source.getText(node.callee);
									const argText = source.getText(spreadArg);
									return fixer.replaceText(node, `Reflect.construct(${ctorText}, ${argText})`);
								}
							: null,
					});
				}
			},
		};
	},
});
