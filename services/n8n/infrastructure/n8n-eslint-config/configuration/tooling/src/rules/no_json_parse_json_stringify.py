"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-json-parse-json-stringify.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:../utils/json.js。导出:NoJsonParseJsonStringifyRule。关键函数/方法:create、CallExpression。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-json-parse-json-stringify.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_json_parse_json_stringify.py

import { isJsonParseCall, isJsonStringifyCall } from '../utils/json.js';
import { ESLintUtils, TSESTree } from '@typescript-eslint/utils';

export const NoJsonParseJsonStringifyRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description:
				'Calls to `JSON.parse(JSON.stringify(arg))` must be replaced with `deepCopy(arg)` from `n8n-workflow`.',
		},
		schema: [],
		messages: {
			noJsonParseJsonStringify: 'Replace with `deepCopy({{ argText }})`',
		},
		fixable: 'code',
	},
	defaultOptions: [],
	create(context) {
		return {
			CallExpression(node) {
				if (isJsonParseCall(node) && isJsonStringifyCall(node)) {
					const [callExpression] = node.arguments;

					if (callExpression.type !== TSESTree.AST_NODE_TYPES.CallExpression) {
						return;
					}

					const { arguments: args } = callExpression;

					if (!Array.isArray(args) || args.length !== 1) return;

					const [arg] = args;

					if (!arg) return;

					const argText = context.sourceCode.getText(arg);

					context.report({
						messageId: 'noJsonParseJsonStringify',
						node,
						data: { argText },
						fix: (fixer) => fixer.replaceText(node, `deepCopy(${argText})`),
					});
				}
			},
		};
	},
});
