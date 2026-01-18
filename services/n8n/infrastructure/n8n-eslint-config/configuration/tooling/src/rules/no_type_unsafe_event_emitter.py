"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/no-type-unsafe-event-emitter.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的模块。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:NoTypeUnsafeEventEmitterRule。关键函数/方法:create、ClassDeclaration。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/no-type-unsafe-event-emitter.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/no_type_unsafe_event_emitter.py

import { ESLintUtils } from '@typescript-eslint/utils';

export const NoTypeUnsafeEventEmitterRule = ESLintUtils.RuleCreator.withoutDocs({
	meta: {
		type: 'problem',
		docs: {
			description: 'Disallow extending from `EventEmitter`, which is not type-safe.',
		},
		messages: {
			noExtendsEventEmitter: 'Extend from the type-safe `TypedEmitter` class instead.',
		},
		schema: [],
	},
	defaultOptions: [],
	create(context) {
		return {
			ClassDeclaration(node) {
				if (
					node.superClass &&
					node.superClass.type === 'Identifier' &&
					node.superClass.name === 'EventEmitter' &&
					node.id?.name !== 'TypedEmitter'
				) {
					context.report({
						node: node.superClass,
						messageId: 'noExtendsEventEmitter',
					});
				}
			},
		};
	},
});
