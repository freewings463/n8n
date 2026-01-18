"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-uncaught-json-parse.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:../utils/json.js。导出:NoUncaughtJsonParseRule。关键函数/方法:create、CallExpression、report。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-uncaught-json-parse.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_uncaught_json_parse.py

import { ESLintUtils } from '@typescript-eslint/utils';
import { isJsonParseCall, isJsonStringifyCall } from '../utils/json.js';

export const NoUncaughtJsonParseRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		hasSuggestions: true,
		docs: {
			description:
				'Calls to `JSON.parse()` must be replaced with `jsonParse()` from `n8n-workflow` or surrounded with a try/catch block.',
		},
		schema: [],
		messages: {
			noUncaughtJsonParse:
				'Use `jsonParse()` from `n8n-workflow` or surround the `JSON.parse()` call with a try/catch block.',
		},
	},
	defaultOptions: [],
	create({ report, sourceCode }) {
		return {
			CallExpression(node) {
				if (!isJsonParseCall(node)) {
					return;
				}

				if (isJsonStringifyCall(node)) {
					return;
				}

				if (
					sourceCode.getAncestors(node).find((node) => node.type === 'TryStatement') !== undefined
				) {
					return;
				}

				// Found a JSON.parse() call not wrapped into a try/catch, so report it
				report({
					messageId: 'noUncaughtJsonParse',
					node,
				});
			},
		};
	},
});
