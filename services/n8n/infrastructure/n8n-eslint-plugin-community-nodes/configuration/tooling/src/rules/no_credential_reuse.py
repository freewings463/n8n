"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-plugin-community-nodes/src/rules/no-credential-reuse.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-plugin-community-nodes/src/rules 的模块。导入/依赖:外部:@typescript-eslint/types、@typescript-eslint/utils/ts-eslint；内部:无；本地:无。导出:NoCredentialReuseRule。关键函数/方法:create、loadPackageCredentials、ClassDeclaration、fix。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-plugin-community-nodes/src/rules/no-credential-reuse.ts -> services/n8n/infrastructure/n8n-eslint-plugin-community-nodes/configuration/tooling/src/rules/no_credential_reuse.py

import { TSESTree } from '@typescript-eslint/types';
import type { ReportSuggestionArray } from '@typescript-eslint/utils/ts-eslint';

import {
	isNodeTypeClass,
	findClassProperty,
	findArrayLiteralProperty,
	extractCredentialNameFromArray,
	findPackageJson,
	readPackageJsonCredentials,
	isFileType,
	findSimilarStrings,
	createRule,
} from '../utils/index.js';

export const NoCredentialReuseRule = createRule({
	name: 'no-credential-reuse',
	meta: {
		type: 'problem',
		docs: {
			description:
				'Prevent credential re-use security issues by ensuring nodes only reference credentials from the same package',
		},
		messages: {
			didYouMean: "Did you mean '{{ suggestedName }}'?",
			useAvailable: "Use available credential '{{ suggestedName }}'",
			credentialNotInPackage:
				'SECURITY: Node references credential "{{ credentialName }}" which is not defined in this package. This creates a security risk as it attempts to reuse credentials from other packages. Nodes can only use credentials from the same package as listed in package.json n8n.credentials field.',
		},
		schema: [],
		hasSuggestions: true,
	},
	defaultOptions: [],
	create(context) {
		if (!isFileType(context.filename, '.node.ts')) {
			return {};
		}

		let packageCredentials: Set<string> | null = null;

		const loadPackageCredentials = (): Set<string> => {
			if (packageCredentials !== null) {
				return packageCredentials;
			}

			const packageJsonPath = findPackageJson(context.filename);
			if (!packageJsonPath) {
				packageCredentials = new Set();
				return packageCredentials;
			}

			packageCredentials = readPackageJsonCredentials(packageJsonPath);
			return packageCredentials;
		};

		return {
			ClassDeclaration(node) {
				if (!isNodeTypeClass(node)) {
					return;
				}

				const descriptionProperty = findClassProperty(node, 'description');
				if (
					!descriptionProperty?.value ||
					descriptionProperty.value.type !== TSESTree.AST_NODE_TYPES.ObjectExpression
				) {
					return;
				}

				const credentialsArray = findArrayLiteralProperty(descriptionProperty.value, 'credentials');
				if (!credentialsArray) {
					return;
				}

				const allowedCredentials = loadPackageCredentials();

				credentialsArray.elements.forEach((element) => {
					const credentialInfo = extractCredentialNameFromArray(element);
					if (credentialInfo && !allowedCredentials.has(credentialInfo.name)) {
						const similarCredentials = findSimilarStrings(credentialInfo.name, allowedCredentials);
						const suggestions: ReportSuggestionArray<
							'didYouMean' | 'useAvailable' | 'credentialNotInPackage'
						> = [];

						for (const similarName of similarCredentials) {
							suggestions.push({
								messageId: 'didYouMean',
								data: { suggestedName: similarName },
								fix(fixer) {
									return fixer.replaceText(credentialInfo.node, `"${similarName}"`);
								},
							});
						}

						if (suggestions.length === 0 && allowedCredentials.size > 0) {
							const availableCredentials = Array.from(allowedCredentials).slice(0, 3);
							for (const availableName of availableCredentials) {
								suggestions.push({
									messageId: 'useAvailable',
									data: { suggestedName: availableName },
									fix(fixer) {
										return fixer.replaceText(credentialInfo.node, `"${availableName}"`);
									},
								});
							}
						}

						context.report({
							node: credentialInfo.node,
							messageId: 'credentialNotInPackage',
							data: {
								credentialName: credentialInfo.name,
							},
							suggest: suggestions,
						});
					}
				});
			},
		};
	},
});
