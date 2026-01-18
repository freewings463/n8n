"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/helpers/state.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools/helpers 的工作流模块。导入/依赖:外部:@langchain/langgraph；内部:n8n-workflow；本地:../types/workflow 等1项。导出:getCurrentWorkflow、getWorkflowState、getCurrentWorkflowFromTaskInput、updateWorkflowConnections、addNodeToWorkflow 等6项。关键函数/方法:getCurrentWorkflow、getWorkflowState、getCurrentWorkflowFromTaskInput、updateWorkflowConnections 等7项。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/helpers/state.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/tools/helpers/state.py

import { getCurrentTaskInput } from '@langchain/langgraph';
import type { INode, IConnection } from 'n8n-workflow';

import type { SimpleWorkflow } from '../../types/workflow';
import type { WorkflowState } from '../../workflow-state';

/**
 * Get the current workflow from state in a type-safe manner
 */
export function getCurrentWorkflow(state: typeof WorkflowState.State): SimpleWorkflow {
	return state.workflowJSON;
}

export function getWorkflowState(): typeof WorkflowState.State {
	return getCurrentTaskInput();
}

/**
 * Get the current workflow from task input
 */
export function getCurrentWorkflowFromTaskInput(): SimpleWorkflow {
	const state = getWorkflowState();
	return getCurrentWorkflow(state);
}

/**
 * Create a state update for workflow connections
 */
export function updateWorkflowConnections(
	connections: SimpleWorkflow['connections'],
): Partial<typeof WorkflowState.State> {
	// Return an operation to merge connections (not replace them)
	return {
		workflowOperations: [{ type: 'mergeConnections', connections }],
	};
}

/**
 * Add a node to the workflow state
 */
export function addNodeToWorkflow(node: INode): Partial<typeof WorkflowState.State> {
	return addNodesToWorkflow([node]);
}

/**
 * Add multiple nodes to the workflow state
 */
export function addNodesToWorkflow(nodes: INode[]): Partial<typeof WorkflowState.State> {
	// Return an operation to add nodes
	return {
		workflowOperations: [{ type: 'addNodes', nodes }],
	};
}

/**
 * Remove a node from the workflow state
 */
export function removeNodeFromWorkflow(nodeId: string): Partial<typeof WorkflowState.State> {
	// Return an operation to remove nodes
	return {
		workflowOperations: [{ type: 'removeNode', nodeIds: [nodeId] }],
	};
}

/**
 * Remove multiple nodes from the workflow state
 */
export function removeNodesFromWorkflow(nodeIds: string[]): Partial<typeof WorkflowState.State> {
	// Return an operation to remove nodes
	return {
		workflowOperations: [{ type: 'removeNode', nodeIds }],
	};
}

/**
 * Update a node in the workflow state
 */
export function updateNodeInWorkflow(
	state: typeof WorkflowState.State,
	nodeId: string,
	updates: Partial<INode>,
): Partial<typeof WorkflowState.State> {
	const existingNode = state.workflowJSON.nodes.find((n) => n.id === nodeId);
	if (!existingNode) {
		return {};
	}

	// Return an operation to update the node
	return {
		workflowOperations: [{ type: 'updateNode', nodeId, updates }],
	};
}

/**
 * Add a connection to the workflow state
 */
export function addConnectionToWorkflow(
	sourceNodeId: string,
	_targetNodeId: string,
	connection: IConnection,
): Partial<typeof WorkflowState.State> {
	return {
		workflowOperations: [
			{
				type: 'mergeConnections',
				connections: {
					[sourceNodeId]: {
						main: [[connection]],
					},
				},
			},
		],
	};
}

/**
 * Remove a connection from the workflow state
 */
export function removeConnectionFromWorkflow(
	sourceNode: string,
	targetNode: string,
	connectionType: string,
	sourceOutputIndex: number,
	targetInputIndex: number,
): Partial<typeof WorkflowState.State> {
	return {
		workflowOperations: [
			{
				type: 'removeConnection',
				sourceNode,
				targetNode,
				connectionType,
				sourceOutputIndex,
				targetInputIndex,
			},
		],
	};
}
