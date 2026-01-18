"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/workflow-node-context.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context 的工作流模块。导入/依赖:外部:无；内部:无；本地:./node-execution-context。导出:LoadWorkflowNodeContext。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/workflow-node-context.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/workflow_node_context.py

import type {
	IGetNodeParameterOptions,
	INode,
	IWorkflowExecuteAdditionalData,
	Workflow,
	IWorkflowNodeContext,
} from 'n8n-workflow';

import { NodeExecutionContext } from './node-execution-context';

export class LoadWorkflowNodeContext extends NodeExecutionContext implements IWorkflowNodeContext {
	// Note that this differs from and does not shadow the function with the
	// same name in `NodeExecutionContext`, as it has the `itemIndex` parameter
	readonly getNodeParameter: IWorkflowNodeContext['getNodeParameter'];

	constructor(workflow: Workflow, node: INode, additionalData: IWorkflowExecuteAdditionalData) {
		super(workflow, node, additionalData, 'internal');
		{
			// We need to cast due to the overloaded IWorkflowNodeContext::getNodeParameter function
			// Which would require us to replicate all overload return types, as TypeScript offers
			// no convenient solution to refer to a set of overloads.
			this.getNodeParameter = ((
				parameterName: string,
				itemIndex: number,
				fallbackValue?: unknown,
				options?: IGetNodeParameterOptions,
			) =>
				this._getNodeParameter(
					parameterName,
					itemIndex,
					fallbackValue,
					options,
				)) as IWorkflowNodeContext['getNodeParameter'];
		}
	}
}
