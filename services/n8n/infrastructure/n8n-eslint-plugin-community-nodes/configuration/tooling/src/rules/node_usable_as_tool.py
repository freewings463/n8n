"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-plugin-community-nodes/src/rules/node-usable-as-tool.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-plugin-community-nodes/src/rules 的模块。导入/依赖:外部:@typescript-eslint/types；内部:无；本地:无。导出:NodeUsableAsToolRule。关键函数/方法:create、ClassDeclaration、fix。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-plugin-community-nodes/src/rules/node-usable-as-tool.ts -> services/n8n/infrastructure/n8n-eslint-plugin-community-nodes/configuration/tooling/src/rules/node_usable_as_tool.py

import { TSESTree } from '@typescript-eslint/types';

import {
	isNodeTypeClass,
	findClassProperty,
	findObjectProperty,
	createRule,
} from '../utils/index.js';

export const NodeUsableAsToolRule = createRule({
	name: 'node-usable-as-tool',
	meta: {
		type: 'problem',
		docs: {
			description: 'Ensure node classes have usableAsTool property',
		},
		messages: {
			missingUsableAsTool:
				'Node class should have usableAsTool property. When in doubt, set it to true.',
		},
		fixable: 'code',
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			ClassDeclaration(node) {
				if (!isNodeTypeClass(node)) {
					return;
				}

				const descriptionProperty = findClassProperty(node, 'description');
				if (!descriptionProperty) {
					return;
				}

				const descriptionValue = descriptionProperty.value;
				if (descriptionValue?.type !== TSESTree.AST_NODE_TYPES.ObjectExpression) {
					return;
				}

				const usableAsToolProperty = findObjectProperty(descriptionValue, 'usableAsTool');

				if (!usableAsToolProperty) {
					context.report({
						node,
						messageId: 'missingUsableAsTool',
						fix(fixer) {
							if (descriptionValue?.type === TSESTree.AST_NODE_TYPES.ObjectExpression) {
								const properties = descriptionValue.properties;
								if (properties.length === 0) {
									const openBrace = descriptionValue.range[0] + 1;
									return fixer.insertTextAfterRange(
										[openBrace, openBrace],
										'\n\t\tusableAsTool: true,',
									);
								} else {
									const lastProperty = properties.at(-1);
									if (lastProperty) {
										return fixer.insertTextAfter(lastProperty, ',\n\t\tusableAsTool: true');
									}
								}
							}

							return null;
						},
					});
				}
			},
		};
	},
});
