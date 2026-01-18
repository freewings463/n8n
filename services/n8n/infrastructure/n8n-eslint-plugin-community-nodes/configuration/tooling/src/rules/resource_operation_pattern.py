"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-plugin-community-nodes/src/rules/resource-operation-pattern.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-plugin-community-nodes/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:ResourceOperationPatternRule。关键函数/方法:create、analyzeNodeDescription、ClassDeclaration。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-plugin-community-nodes/src/rules/resource-operation-pattern.ts -> services/n8n/infrastructure/n8n-eslint-plugin-community-nodes/configuration/tooling/src/rules/resource_operation_pattern.py

import type { TSESTree } from '@typescript-eslint/utils';
import { AST_NODE_TYPES } from '@typescript-eslint/utils';

import {
	isNodeTypeClass,
	findClassProperty,
	findObjectProperty,
	getStringLiteralValue,
	isFileType,
	createRule,
} from '../utils/index.js';

export const ResourceOperationPatternRule = createRule({
	name: 'resource-operation-pattern',
	meta: {
		type: 'problem',
		docs: {
			description: 'Enforce proper resource/operation pattern for better UX in n8n nodes',
		},
		messages: {
			tooManyOperationsWithoutResources:
				'Node has {{ operationCount }} operations without resources. Use resources to organize operations when there are more than 5 operations.',
		},
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		if (!isFileType(context.filename, '.node.ts')) {
			return {};
		}

		const analyzeNodeDescription = (descriptionValue: TSESTree.Expression | null): void => {
			if (!descriptionValue || descriptionValue.type !== AST_NODE_TYPES.ObjectExpression) {
				return;
			}

			const propertiesProperty = findObjectProperty(descriptionValue, 'properties');
			if (
				!propertiesProperty?.value ||
				propertiesProperty.value.type !== AST_NODE_TYPES.ArrayExpression
			) {
				return;
			}

			const propertiesArray = propertiesProperty.value;
			let hasResources = false;
			let operationCount = 0;
			let operationNode: TSESTree.Node | null = null;

			for (const property of propertiesArray.elements) {
				if (!property || property.type !== AST_NODE_TYPES.ObjectExpression) {
					continue;
				}

				const nameProperty = findObjectProperty(property, 'name');
				const typeProperty = findObjectProperty(property, 'type');

				const name = nameProperty ? getStringLiteralValue(nameProperty.value) : null;
				const type = typeProperty ? getStringLiteralValue(typeProperty.value) : null;

				if (!name || !type) {
					continue;
				}

				if (name === 'resource' && type === 'options') {
					hasResources = true;
				}

				if (name === 'operation' && type === 'options') {
					operationNode = property;
					const optionsProperty = findObjectProperty(property, 'options');
					if (optionsProperty?.value?.type === AST_NODE_TYPES.ArrayExpression) {
						operationCount = optionsProperty.value.elements.length;
					}
				}
			}

			if (operationCount > 5 && !hasResources && operationNode) {
				context.report({
					node: operationNode,
					messageId: 'tooManyOperationsWithoutResources',
					data: {
						operationCount: operationCount.toString(),
					},
				});
			}
		};

		return {
			ClassDeclaration(node) {
				if (!isNodeTypeClass(node)) {
					return;
				}

				const descriptionProperty = findClassProperty(node, 'description');
				if (!descriptionProperty) {
					return;
				}

				analyzeNodeDescription(descriptionProperty.value);
			},
		};
	},
});
