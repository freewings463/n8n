"""
MIGRATION-META:
  source_path: packages/cli/src/utils/object-to-error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/utils 的工具。导入/依赖:外部:无；内部:@n8n/backend-common、n8n-workflow；本地:无。导出:objectToError。关键函数/方法:objectToError、isObjectLiteral。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/utils/object-to-error.ts -> services/n8n/application/cli/services/utils/object_to_error.py

import { isObjectLiteral } from '@n8n/backend-common';
import { NodeOperationError } from 'n8n-workflow';
import type { Workflow } from 'n8n-workflow';

/**
 * Optional properties that should be propagated from an error object to the new Error instance.
 */
const errorProperties = ['description', 'stack', 'executionId', 'workflowId'];

export function objectToError(errorObject: unknown, workflow: Workflow): Error {
	// TODO: Expand with other error types
	if (errorObject instanceof Error) {
		// If it's already an Error instance, return it as is.
		return errorObject;
	} else if (
		isObjectLiteral(errorObject) &&
		'message' in errorObject &&
		typeof errorObject.message === 'string'
	) {
		// If it's an object with a 'message' property, create a new Error instance.
		let error: Error | undefined;
		if (
			'node' in errorObject &&
			isObjectLiteral(errorObject.node) &&
			typeof errorObject.node.name === 'string'
		) {
			const node = workflow.getNode(errorObject.node.name);

			if (node) {
				error = new NodeOperationError(
					node,
					errorObject as unknown as Error,
					errorObject as object,
				);
			}
		}

		if (error === undefined) {
			error = new Error(errorObject.message);
		}

		for (const field of errorProperties) {
			if (field in errorObject && errorObject[field]) {
				// Not all errors contain these properties
				(error as unknown as Record<string, unknown>)[field] = errorObject[field];
			}
		}

		return error;
	} else {
		// If it's neither an Error nor an object with a 'message' property, create a generic Error.
		return new Error('An error occurred');
	}
}
