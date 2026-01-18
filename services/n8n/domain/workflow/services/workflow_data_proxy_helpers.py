"""
MIGRATION-META:
  source_path: packages/workflow/src/workflow-data-proxy-helpers.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流工具。导入/依赖:外部:无；内部:无；本地:.。导出:getPinDataIfManualExecution。关键函数/方法:getPinDataIfManualExecution。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/workflow-data-proxy-helpers.ts -> services/n8n/domain/workflow/services/workflow_data_proxy_helpers.py

import type { INodeExecutionData, Workflow, WorkflowExecuteMode } from '.';

export function getPinDataIfManualExecution(
	workflow: Workflow,
	nodeName: string,
	mode: WorkflowExecuteMode,
): INodeExecutionData[] | undefined {
	if (mode !== 'manual') {
		return undefined;
	}
	return workflow.getPinDataOfNode(nodeName);
}
