"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Code/JsCodeValidator.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Code 的节点。导入/依赖:外部:无；内部:无；本地:./ValidationError。导出:validateNoDisallowedMethodsInRunForEach、mapItemsNotDefinedErrorIfNeededForRunForAll、mapItemNotDefinedErrorIfNeededForRunForEach。关键函数/方法:validateNoDisallowedMethodsInRunForEach、mapItemsNotDefinedErrorIfNeededForRunForAll、mapItemNotDefinedErrorIfNeededForRunForEach。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Code/JsCodeValidator.ts -> services/n8n/tests/nodes-base/unit/nodes/Code/JsCodeValidator.py

import { ValidationError } from './ValidationError';

/**
 * Validates that no disallowed methods are used in the
 * runCodeForEachItem JS code. Throws `ValidationError` if
 * a disallowed method is found.
 */
export function validateNoDisallowedMethodsInRunForEach(code: string, itemIndex: number) {
	const match = code.match(/\$input\.(?<disallowedMethod>first|last|all|itemMatching)/);

	if (match?.groups?.disallowedMethod) {
		const { disallowedMethod } = match.groups;

		const lineNumber =
			code.split('\n').findIndex((line) => {
				line = line.trimStart();
				return (
					line.includes(disallowedMethod) &&
					!line.startsWith('//') &&
					!line.startsWith('/*') &&
					!line.startsWith('*')
				);
			}) + 1;

		const disallowedMethodFound = lineNumber !== 0;

		if (disallowedMethodFound) {
			throw new ValidationError({
				message: `Can't use .${disallowedMethod}() here`,
				description: "This is only available in 'Run Once for All Items' mode",
				itemIndex,
				lineNumber,
			});
		}
	}
}

/**
 * Checks if the error message indicates that `items` is not defined and
 * modifies the error message to suggest using `$input.all()`.
 */
export function mapItemsNotDefinedErrorIfNeededForRunForAll(code: string, error: Error) {
	// anticipate user expecting `items` to pre-exist as in Function Item node
	if (error.message === 'items is not defined' && !/(let|const|var) +items +=/.test(code)) {
		const quoted = error.message.replace('items', '`items`');
		error.message = quoted + '. Did you mean `$input.all()`?';
	}
}

/**
 * Maps the "item is not defined" error message to provide a more helpful suggestion
 * for users who may expect `items` to pre-exist
 */
export function mapItemNotDefinedErrorIfNeededForRunForEach(code: string, error: Error) {
	// anticipate user expecting `items` to pre-exist as in Function Item node
	if (error.message === 'item is not defined' && !/(let|const|var) +item +=/.test(code)) {
		const quoted = error.message.replace('item', '`item`');
		error.message = quoted + '. Did you mean `$input.item.json`?';
	}
}
