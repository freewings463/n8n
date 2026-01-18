"""
MIGRATION-META:
  source_path: packages/core/src/node-execute-functions.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src 的模块。导入/依赖:外部:无；内部:无；本地:./execution-engine/node-execution-context。导出:getExecutePollFunctions、getExecuteTriggerFunctions。关键函数/方法:getExecutePollFunctions、getExecuteTriggerFunctions。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core src/* defaulted to execution engine application services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/node-execute-functions.ts -> services/n8n/application/core/services/execution_engine/node_execute_functions.py

import type {
	INode,
	IPollFunctions,
	ITriggerFunctions,
	IWorkflowExecuteAdditionalData,
	Workflow,
	WorkflowActivateMode,
	WorkflowExecuteMode,
} from 'n8n-workflow';

import { PollContext, TriggerContext } from './execution-engine/node-execution-context';

/**
 * Returns the execute functions the poll nodes have access to.
 */
// TODO: Check if I can get rid of: additionalData, and so then maybe also at ActiveWorkflowManager.add
export function getExecutePollFunctions(
	workflow: Workflow,
	node: INode,
	additionalData: IWorkflowExecuteAdditionalData,
	mode: WorkflowExecuteMode,
	activation: WorkflowActivateMode,
): IPollFunctions {
	return new PollContext(workflow, node, additionalData, mode, activation);
}

/**
 * Returns the execute functions the trigger nodes have access to.
 */
// TODO: Check if I can get rid of: additionalData, and so then maybe also at ActiveWorkflowManager.add
export function getExecuteTriggerFunctions(
	workflow: Workflow,
	node: INode,
	additionalData: IWorkflowExecuteAdditionalData,
	mode: WorkflowExecuteMode,
	activation: WorkflowActivateMode,
): ITriggerFunctions {
	return new TriggerContext(workflow, node, additionalData, mode, activation);
}
