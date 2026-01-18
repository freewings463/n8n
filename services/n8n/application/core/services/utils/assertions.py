"""
MIGRATION-META:
  source_path: packages/core/src/utils/assertions.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:assertExecutionDataExists。关键函数/方法:assertExecutionDataExists。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core utility helpers -> application/services/utils
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/utils/assertions.ts -> services/n8n/application/core/services/utils/assertions.py

import {
	type IRunExecutionData,
	type IWorkflowExecuteAdditionalData,
	UnexpectedError,
	type Workflow,
	type WorkflowExecuteMode,
} from 'n8n-workflow';

export function assertExecutionDataExists(
	executionData: IRunExecutionData['executionData'],
	workflow: Workflow,
	additionalData: IWorkflowExecuteAdditionalData,
	mode: WorkflowExecuteMode,
): asserts executionData is NonNullable<IRunExecutionData['executionData']> {
	if (!executionData) {
		throw new UnexpectedError('Failed to run workflow due to missing execution data', {
			extra: {
				workflowId: workflow.id,
				executionId: additionalData.executionId,
				mode,
			},
		});
	}
}
