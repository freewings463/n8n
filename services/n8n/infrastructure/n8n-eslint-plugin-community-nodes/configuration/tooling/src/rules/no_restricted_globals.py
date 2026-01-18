"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-plugin-community-nodes/src/rules/no-restricted-globals.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-plugin-community-nodes/src/rules 的模块。导入/依赖:外部:@typescript-eslint/types、@typescript-eslint/utils；内部:无；本地:../utils/index.js。导出:NoRestrictedGlobalsRule。关键函数/方法:create、checkReference、Program。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-plugin-community-nodes/src/rules/no-restricted-globals.ts -> services/n8n/infrastructure/n8n-eslint-plugin-community-nodes/configuration/tooling/src/rules/no_restricted_globals.py

import { TSESTree } from '@typescript-eslint/types';
import type { TSESLint } from '@typescript-eslint/utils';

import { createRule } from '../utils/index.js';

const restrictedGlobals = [
	'clearInterval',
	'clearTimeout',
	'global',
	'globalThis',
	'process',
	'setInterval',
	'setTimeout',
	'setImmediate',
	'clearImmediate',
	'__dirname',
	'__filename',
];

export const NoRestrictedGlobalsRule = createRule({
	name: 'no-restricted-globals',
	meta: {
		type: 'problem',
		docs: {
			description: 'Disallow usage of restricted global variables in community nodes.',
		},
		messages: {
			restrictedGlobal: "Use of restricted global '{{ name }}' is not allowed",
		},
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		function checkReference(ref: TSESLint.Scope.Reference, name: string) {
			const { parent } = ref.identifier;

			// Skip property access (like console.process - we want process.exit but not obj.process)
			if (
				parent?.type === TSESTree.AST_NODE_TYPES.MemberExpression &&
				parent.property === ref.identifier &&
				!parent.computed
			) {
				return;
			}

			context.report({
				node: ref.identifier,
				messageId: 'restrictedGlobal',
				data: { name },
			});
		}

		return {
			Program() {
				const globalScope = context.sourceCode.getScope(context.sourceCode.ast);

				const allReferences = [
					...globalScope.variables
						.filter(
							(variable) => restrictedGlobals.includes(variable.name) && variable.defs.length === 0, // No definitions means it's a global
						)
						.flatMap((variable) =>
							variable.references.map((ref) => ({ ref, name: variable.name })),
						),
					...globalScope.through
						.filter((ref) => restrictedGlobals.includes(ref.identifier.name))
						.map((ref) => ({ ref, name: ref.identifier.name })),
				];

				allReferences.forEach(({ ref, name }) => checkReference(ref, name));
			},
		};
	},
});
