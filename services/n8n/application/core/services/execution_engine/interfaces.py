"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/interfaces.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine 的执行模块。导入/依赖:外部:无；内部:无；本地:无。导出:IGetExecutePollFunctions、IGetExecuteTriggerFunctions。关键函数/方法:无。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/interfaces.ts -> services/n8n/application/core/services/execution_engine/interfaces.py

import type {
	INode,
	IPollFunctions,
	ITriggerFunctions,
	IWorkflowExecuteAdditionalData,
	Workflow,
	WorkflowActivateMode,
	WorkflowExecuteMode,
} from 'n8n-workflow';

export interface IGetExecutePollFunctions {
	(
		workflow: Workflow,
		node: INode,
		additionalData: IWorkflowExecuteAdditionalData,
		mode: WorkflowExecuteMode,
		activation: WorkflowActivateMode,
	): IPollFunctions;
}

export interface IGetExecuteTriggerFunctions {
	(
		workflow: Workflow,
		node: INode,
		additionalData: IWorkflowExecuteAdditionalData,
		mode: WorkflowExecuteMode,
		activation: WorkflowActivateMode,
	): ITriggerFunctions;
}
