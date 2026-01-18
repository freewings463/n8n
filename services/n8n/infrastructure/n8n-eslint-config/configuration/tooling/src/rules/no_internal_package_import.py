"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-internal-package-import.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoInternalPackageImportRule。关键函数/方法:create、ImportDeclaration。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-internal-package-import.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_internal_package_import.py

import { ESLintUtils } from '@typescript-eslint/utils';

export const NoInternalPackageImportRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description: 'Disallow imports from internal package paths (e.g. `@n8n/pkg/src/...`).',
		},
		messages: {
			noInternalPackageImport:
				'Import from "{{ packageRoot }}", not from the internal `/src/` path.',
		},
		fixable: 'code',
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		const INTERNAL_IMPORT_REGEX = /^(?<packageRoot>@n8n\/[^/]+)\/src\//;

		return {
			ImportDeclaration(node) {
				if (typeof node.source.type !== 'string') return;

				const match = node.source.value.match(INTERNAL_IMPORT_REGEX);

				if (!match?.groups) return;

				const { packageRoot } = match.groups;

				context.report({
					node: node.source,
					messageId: 'noInternalPackageImport',
					fix: (fixer) => fixer.replaceText(node.source, `"${packageRoot}"`),
					data: { packageRoot },
				});
			},
		};
	},
});
