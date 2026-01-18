"""
MIGRATION-META:
  source_path: packages/workflow/src/node-parameters/rename-node-utils.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/node-parameters 的工作流模块。导入/依赖:外部:无；内部:无；本地:../interfaces。导出:renameFormFields。关键函数/方法:renameFormFields。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/node-parameters/rename-node-utils.ts -> services/n8n/domain/workflow/services/node-parameters/rename_node_utils.py

import type { INode, NodeParameterValueType } from '../interfaces';

export function renameFormFields(
	node: INode,
	renameField: (v: NodeParameterValueType) => NodeParameterValueType,
): void {
	const formFields = node.parameters?.formFields;

	const values =
		formFields &&
		typeof formFields === 'object' &&
		'values' in formFields &&
		typeof formFields.values === 'object' &&
		// TypeScript thinks this is `Array.values` and gets very confused here
		// eslint-disable-next-line @typescript-eslint/unbound-method
		Array.isArray(formFields.values)
			? // eslint-disable-next-line @typescript-eslint/unbound-method
				(formFields.values ?? [])
			: [];

	for (const formFieldValue of values) {
		if (!formFieldValue || typeof formFieldValue !== 'object') continue;
		if ('fieldType' in formFieldValue && formFieldValue.fieldType === 'html') {
			if ('html' in formFieldValue) {
				formFieldValue.html = renameField(formFieldValue.html);
			}
		}
	}
}
