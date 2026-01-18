"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-untyped-config-class-field.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoUntypedConfigClassFieldRule。关键函数/方法:create、PropertyDefinition。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-untyped-config-class-field.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_untyped_config_class_field.py

import { ESLintUtils } from '@typescript-eslint/utils';

export const NoUntypedConfigClassFieldRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description: 'Enforce explicit typing of config class fields',
		},
		messages: {
			noUntypedConfigClassField:
				'Class field must have an explicit type annotation, e.g. `field: type = value`. See: https://github.com/n8n-io/n8n/pull/10433',
		},
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			PropertyDefinition(node) {
				if (!node.typeAnnotation) {
					context.report({ node: node.key, messageId: 'noUntypedConfigClassField' });
				}
			},
		};
	},
});
