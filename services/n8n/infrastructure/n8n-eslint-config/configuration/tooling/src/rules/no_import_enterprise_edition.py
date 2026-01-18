"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-import-enterprise-edition.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoImportEnterpriseEditionRule。关键函数/方法:create、ImportDeclaration。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-import-enterprise-edition.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_import_enterprise_edition.py

import { ESLintUtils } from '@typescript-eslint/utils';

export const NoImportEnterpriseEditionRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description:
				'Disallow imports from .ee directories in non-enterprise code. Only code in .ee directories can import from other .ee directories.',
		},
		messages: {
			noImportEnterpriseEdition:
				'Non-enterprise code cannot import from .ee directories. Only code in .ee directories can import from other .ee directories.',
		},
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		const filename = context.filename;
		const isEnterpriseEditionFile = filename.includes('.ee/');
		const isIntegrationTestFile = filename.includes('packages/cli/test/integration/');

		if (isEnterpriseEditionFile || isIntegrationTestFile) {
			return {};
		}

		return {
			ImportDeclaration(node) {
				const importPath = node.source.value;

				const isEnterpriseEditionImport = importPath.includes('.ee/');

				if (isEnterpriseEditionImport) {
					context.report({
						node: node.source,
						messageId: 'noImportEnterpriseEdition',
					});
				}
			},
		};
	},
});
