"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-plugin-community-nodes/src/rules/no-restricted-imports.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-plugin-community-nodes/src/rules 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:NoRestrictedImportsRule。关键函数/方法:create、isModuleAllowed、ImportDeclaration、ImportExpression、CallExpression。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-plugin-community-nodes/src/rules/no-restricted-imports.ts -> services/n8n/infrastructure/n8n-eslint-plugin-community-nodes/configuration/tooling/src/rules/no_restricted_imports.py

import {
	getModulePath,
	isDirectRequireCall,
	isRequireMemberCall,
	createRule,
} from '../utils/index.js';

const allowedModules = [
	'n8n-workflow',
	'lodash',
	'moment',
	'p-limit',
	'luxon',
	'zod',
	'crypto',
	'node:crypto',
];

const isModuleAllowed = (modulePath: string): boolean => {
	if (modulePath.startsWith('./') || modulePath.startsWith('../')) return true;

	const moduleName = modulePath.startsWith('@')
		? modulePath.split('/').slice(0, 2).join('/')
		: modulePath.split('/')[0];
	if (!moduleName) return true;
	return allowedModules.includes(moduleName);
};

export const NoRestrictedImportsRule = createRule({
	name: 'no-restricted-imports',
	meta: {
		type: 'problem',
		docs: {
			description: 'Disallow usage of restricted imports in community nodes.',
		},
		messages: {
			restrictedImport:
				"Import of '{{ modulePath }}' is not allowed. n8n Cloud does not allow community nodes with dependencies.",
			restrictedRequire:
				"Require of '{{ modulePath }}' is not allowed. n8n Cloud does not allow community nodes with dependencies.",
			restrictedDynamicImport:
				"Dynamic import of '{{ modulePath }}' is not allowed. n8n Cloud does not allow community nodes with dependencies.",
		},
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			ImportDeclaration(node) {
				const modulePath = getModulePath(node.source);
				if (modulePath && !isModuleAllowed(modulePath)) {
					context.report({
						node,
						messageId: 'restrictedImport',
						data: {
							modulePath,
						},
					});
				}
			},

			ImportExpression(node) {
				const modulePath = getModulePath(node.source);
				if (modulePath && !isModuleAllowed(modulePath)) {
					context.report({
						node,
						messageId: 'restrictedDynamicImport',
						data: {
							modulePath,
						},
					});
				}
			},

			CallExpression(node) {
				if (isDirectRequireCall(node) || isRequireMemberCall(node)) {
					const modulePath = getModulePath(node.arguments[0] ?? null);
					if (modulePath && !isModuleAllowed(modulePath)) {
						context.report({
							node,
							messageId: 'restrictedRequire',
							data: {
								modulePath,
							},
						});
					}
				}
			},
		};
	},
});
