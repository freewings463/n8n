"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/misplaced-n8n-typeorm-import.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:MisplacedN8nTypeormImportRule。关键函数/方法:create、ImportDeclaration。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/misplaced-n8n-typeorm-import.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/misplaced_n8n_typeorm_import.py

import { ESLintUtils } from '@typescript-eslint/utils';

export const MisplacedN8nTypeormImportRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description: 'Ensure `@n8n/typeorm` is imported only from within the `@n8n/db` package.',
		},
		messages: {
			moveImport: 'Please move this import to `@n8n/db`.',
		},
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			ImportDeclaration(node) {
				if (node.source.value === '@n8n/typeorm' && !context.filename.includes('@n8n/db')) {
					context.report({ node, messageId: 'moveImport' });
				}
			},
		};
	},
});
