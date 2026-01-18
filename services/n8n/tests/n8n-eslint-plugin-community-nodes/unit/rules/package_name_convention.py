"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-plugin-community-nodes/src/rules/package-name-convention.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-plugin-community-nodes/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils、@typescript-eslint/utils/ts-eslint；内部:无；本地:../utils/index.js。导出:PackageNameConventionRule。关键函数/方法:create、ObjectExpression、fix、isValidPackageName、generatePackageNameSuggestions、cleanName。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-plugin-community-nodes/src/rules/package-name-convention.ts -> services/n8n/tests/n8n-eslint-plugin-community-nodes/unit/rules/package_name_convention.py

import type { TSESTree } from '@typescript-eslint/utils';
import { AST_NODE_TYPES } from '@typescript-eslint/utils';
import type { ReportSuggestionArray } from '@typescript-eslint/utils/ts-eslint';

import { createRule } from '../utils/index.js';

export const PackageNameConventionRule = createRule({
	name: 'package-name-convention',
	meta: {
		type: 'problem',
		docs: {
			description: 'Enforce correct package naming convention for n8n community nodes',
		},
		messages: {
			renameTo: "Rename to '{{suggestedName}}'",
			invalidPackageName:
				'Package name "{{ packageName }}" must follow the convention "n8n-nodes-[PACKAGE-NAME]" or "@[AUTHOR]/n8n-nodes-[PACKAGE-NAME]"',
		},
		schema: [],
		hasSuggestions: true,
	},
	defaultOptions: [],
	create(context) {
		if (!context.filename.endsWith('package.json')) {
			return {};
		}

		return {
			ObjectExpression(node: TSESTree.ObjectExpression) {
				if (node.parent?.type === AST_NODE_TYPES.Property) {
					return;
				}

				const nameProperty = node.properties.find(
					(property) =>
						property.type === AST_NODE_TYPES.Property &&
						property.key.type === AST_NODE_TYPES.Literal &&
						property.key.value === 'name',
				);

				if (!nameProperty || nameProperty.type !== AST_NODE_TYPES.Property) {
					return;
				}

				if (nameProperty.value.type !== AST_NODE_TYPES.Literal) {
					return;
				}

				const packageName = nameProperty.value.value;
				const packageNameStr = typeof packageName === 'string' ? packageName : null;

				if (!packageNameStr || !isValidPackageName(packageNameStr)) {
					const suggestions: ReportSuggestionArray<'invalidPackageName' | 'renameTo'> = [];

					// Generate package name suggestions if we have a valid string
					if (packageNameStr) {
						const suggestedNames = generatePackageNameSuggestions(packageNameStr);
						for (const suggestedName of suggestedNames) {
							suggestions.push({
								messageId: 'renameTo',
								data: { suggestedName },
								fix(fixer) {
									return fixer.replaceText(nameProperty.value, `"${suggestedName}"`);
								},
							});
						}
					}

					context.report({
						node: nameProperty,
						messageId: 'invalidPackageName',
						data: {
							packageName: packageNameStr ?? 'undefined',
						},
						suggest: suggestions,
					});
				}
			},
		};
	},
});

function isValidPackageName(name: string): boolean {
	const unscoped = /^n8n-nodes-.+$/;
	const scoped = /^@.+\/n8n-nodes-.+$/;
	return unscoped.test(name) || scoped.test(name);
}

function generatePackageNameSuggestions(invalidName: string): string[] {
	const cleanName = (name: string) => {
		return name
			.replace(/^nodes?-?n8n-?/, '')
			.replace(/^n8n-/, '')
			.replace(/^nodes?-?/, '')
			.replace(/^node-/, '')
			.replace(/-nodes$/, '');
	};

	if (invalidName.startsWith('@')) {
		const [scope, packagePart] = invalidName.split('/');
		const clean = cleanName(packagePart ?? '');
		return clean ? [`${scope}/n8n-nodes-${clean}`] : [];
	}

	const clean = cleanName(invalidName);
	return clean ? [`n8n-nodes-${clean}`] : [];
}
