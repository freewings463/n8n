"""
MIGRATION-META:
  source_path: packages/workflow/src/metadata-utils.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流模块。导入/依赖:外部:无；内部:无；本地:.、./utils。导出:parseErrorMetadata。关键函数/方法:responseHasSubworkflowData、parseErrorResponseWorkflowMetadata、parseErrorMetadata。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/metadata-utils.ts -> services/n8n/domain/workflow/services/metadata_utils.py

import type { ITaskMetadata } from '.';
import { hasKey } from './utils';

function responseHasSubworkflowData(
	response: unknown,
): response is { executionId: string; workflowId: string } {
	return ['executionId', 'workflowId'].every(
		(x) => hasKey(response, x) && typeof response[x] === 'string',
	);
}

type ISubWorkflowMetadata = Required<Pick<ITaskMetadata, 'subExecution' | 'subExecutionsCount'>>;

function parseErrorResponseWorkflowMetadata(response: unknown): ISubWorkflowMetadata | undefined {
	if (!responseHasSubworkflowData(response)) return undefined;

	return {
		subExecution: {
			executionId: response.executionId,
			workflowId: response.workflowId,
		},
		subExecutionsCount: 1,
	};
}

export function parseErrorMetadata(error: unknown): ISubWorkflowMetadata | undefined {
	if (hasKey(error, 'errorResponse')) {
		return parseErrorResponseWorkflowMetadata(error.errorResponse);
	}

	// This accounts for cases where the backend attaches the properties on plain errors
	// e.g. from custom nodes throwing literal `Error` or `ApplicationError` objects directly
	return parseErrorResponseWorkflowMetadata(error);
}
