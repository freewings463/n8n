"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/local-load-options-context.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context 的执行模块。导入/依赖:外部:lodash/get；内部:n8n-workflow；本地:./workflow-node-context。导出:LocalLoadOptionsContext。关键函数/方法:getWorkflowNodeContext、selectedWorkflowNode、getCurrentNodeParameter。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/local-load-options-context.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/local_load_options_context.py

import get from 'lodash/get';
import { ApplicationError, resolveRelativePath, Workflow } from 'n8n-workflow';
import type {
	INodeParameterResourceLocator,
	IWorkflowExecuteAdditionalData,
	NodeParameterValueType,
	ILocalLoadOptionsFunctions,
	IWorkflowLoader,
	IWorkflowNodeContext,
	INodeTypes,
} from 'n8n-workflow';

import { LoadWorkflowNodeContext } from './workflow-node-context';

export class LocalLoadOptionsContext implements ILocalLoadOptionsFunctions {
	constructor(
		private nodeTypes: INodeTypes,
		private additionalData: IWorkflowExecuteAdditionalData,
		private path: string,
		private workflowLoader: IWorkflowLoader,
	) {}

	async getWorkflowNodeContext(
		nodeType: string,
		useActiveVersion: boolean = false,
	): Promise<IWorkflowNodeContext | null> {
		const { value: workflowId } = this.getCurrentNodeParameter(
			'workflowId',
		) as INodeParameterResourceLocator;

		if (typeof workflowId !== 'string' || !workflowId) {
			throw new ApplicationError(`No workflowId parameter defined on node of type "${nodeType}"!`);
		}

		const dbWorkflow = await this.workflowLoader.get(workflowId);

		if (useActiveVersion && !dbWorkflow.activeVersion) {
			throw new ApplicationError(`No active version found for workflow "${workflowId}"!`);
		}

		const selectedWorkflowNode = (
			useActiveVersion ? dbWorkflow.activeVersion!.nodes : dbWorkflow.nodes
		).find((node) => node.type === nodeType);

		if (selectedWorkflowNode) {
			const selectedSingleNodeWorkflow = new Workflow({
				id: dbWorkflow.id,
				name: dbWorkflow.name,
				nodes: [selectedWorkflowNode],
				connections: {},
				active: false,
				nodeTypes: this.nodeTypes,
			});

			const workflowAdditionalData = {
				...this.additionalData,
				currentNodeParameters: selectedWorkflowNode.parameters,
			};

			return new LoadWorkflowNodeContext(
				selectedSingleNodeWorkflow,
				selectedWorkflowNode,
				workflowAdditionalData,
			);
		}

		return null;
	}

	getCurrentNodeParameter(parameterPath: string): NodeParameterValueType | object | undefined {
		const nodeParameters = this.additionalData.currentNodeParameters;

		parameterPath = resolveRelativePath(this.path, parameterPath);

		return get(nodeParameters, parameterPath);
	}
}
