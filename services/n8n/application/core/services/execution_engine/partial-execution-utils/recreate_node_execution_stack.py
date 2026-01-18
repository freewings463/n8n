"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/partial-execution-utils/recreate-node-execution-stack.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/partial-execution-utils 的执行模块。导入/依赖:外部:assert/strict；内部:无；本地:./directed-graph、./get-incoming-data、./get-source-data-groups。导出:addWaitingExecution、addWaitingExecutionSource、recreateNodeExecutionStack。关键函数/方法:addWaitingExecution、addWaitingExecutionSource、recreateNodeExecutionStack。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/partial-execution-utils/recreate-node-execution-stack.ts -> services/n8n/application/core/services/execution_engine/partial-execution-utils/recreate_node_execution_stack.py

import * as a from 'assert/strict';
import {
	NodeConnectionTypes,
	type NodeConnectionType,
	type IExecuteData,
	type INode,
	type INodeExecutionData,
	type IPinData,
	type IRunData,
	type ISourceData,
	type ITaskDataConnectionsSource,
	type IWaitingForExecution,
	type IWaitingForExecutionSource,
} from 'n8n-workflow';

import type { DirectedGraph } from './directed-graph';
import { getIncomingDataFromAnyRun } from './get-incoming-data';
import { getSourceDataGroups } from './get-source-data-groups';

export function addWaitingExecution(
	waitingExecution: IWaitingForExecution,
	nodeName: string,
	runIndex: number,
	inputType: NodeConnectionType,
	inputIndex: number,
	executionData: INodeExecutionData[] | null,
) {
	const waitingExecutionObject = waitingExecution[nodeName] ?? {};
	const taskDataConnections = waitingExecutionObject[runIndex] ?? {};
	const executionDataList = taskDataConnections[inputType] ?? [];

	executionDataList[inputIndex] = executionData;

	taskDataConnections[inputType] = executionDataList;
	waitingExecutionObject[runIndex] = taskDataConnections;
	waitingExecution[nodeName] = waitingExecutionObject;
}

export function addWaitingExecutionSource(
	waitingExecutionSource: IWaitingForExecutionSource,
	nodeName: string,
	runIndex: number,
	inputType: NodeConnectionType,
	inputIndex: number,
	sourceData: ISourceData | null,
) {
	const waitingExecutionSourceObject = waitingExecutionSource[nodeName] ?? {};
	const taskDataConnectionsSource = waitingExecutionSourceObject[runIndex] ?? {};
	const sourceDataList = taskDataConnectionsSource[inputType] ?? [];

	sourceDataList[inputIndex] = sourceData;

	taskDataConnectionsSource[inputType] = sourceDataList;
	waitingExecutionSourceObject[runIndex] = taskDataConnectionsSource;
	waitingExecutionSource[nodeName] = waitingExecutionSourceObject;
}

/**
 * Recreates the node execution stack, waiting executions and waiting
 * execution sources from a directed graph, start nodes, the destination node,
 * run and pinned data.
 *
 * This function aims to be able to recreate the internal state of the
 * WorkflowExecute class at any point of time during an execution based on the
 * data that is already available. Specifically it will recreate the
 * `WorkflowExecute.runExecutionData.executionData` properties.
 *
 * This allows "restarting" an execution and having it only execute what's
 * necessary to be able to execute the destination node accurately, e.g. as
 * close as possible to what would happen in a production execution.
 */
export function recreateNodeExecutionStack(
	graph: DirectedGraph,
	startNodes: Set<INode>,
	runData: IRunData,
	pinData: IPinData,
): {
	nodeExecutionStack: IExecuteData[];
	waitingExecution: IWaitingForExecution;
	waitingExecutionSource: IWaitingForExecutionSource;
} {
	// Validate invariants.

	// The graph needs to be free of disabled nodes. If it's not it hasn't been
	// passed through findSubgraph.
	for (const node of graph.getNodes().values()) {
		a.notEqual(
			node.disabled,
			true,
			`Graph contains disabled nodes. This is not supported. Make sure to pass the graph through "findSubgraph" before calling "recreateNodeExecutionStack". The node in question is "${node.name}"`,
		);
	}

	// Initialize the nodeExecutionStack and waitingExecution with
	// the data from runData
	const nodeExecutionStack: IExecuteData[] = [];
	const waitingExecution: IWaitingForExecution = {};
	const waitingExecutionSource: IWaitingForExecutionSource = {};

	for (const startNode of startNodes) {
		const incomingStartNodeConnections = graph
			.getDirectParentConnections(startNode)
			.filter((c) => c.type === NodeConnectionTypes.Main);

		let incomingData: INodeExecutionData[][] = [];
		let incomingSourceData: ITaskDataConnectionsSource | null = null;

		if (incomingStartNodeConnections.length === 0) {
			incomingData.push([{ json: {} }]);

			const executeData: IExecuteData = {
				node: startNode,
				data: { main: incomingData },
				source: incomingSourceData,
			};

			nodeExecutionStack.push(executeData);
		} else {
			const sourceDataSets = getSourceDataGroups(graph, startNode, runData, pinData);

			for (const sourceData of sourceDataSets) {
				if (sourceData.complete) {
					// All incoming connections have data, so let's put the node on the
					// stack!
					incomingData = [];

					incomingSourceData = { main: [] };

					for (const incomingConnection of sourceData.connections) {
						let runIndex = 0;
						const sourceNode = incomingConnection.from;

						if (pinData[sourceNode.name]) {
							incomingData.push(pinData[sourceNode.name]);
						} else {
							a.ok(
								runData[sourceNode.name],
								`Start node(${incomingConnection.to.name}) has an incoming connection with no run or pinned data. This is not supported. The connection in question is "${sourceNode.name}->${startNode.name}". Are you sure the start nodes come from the "findStartNodes" function?`,
							);

							const nodeIncomingData = getIncomingDataFromAnyRun(
								runData,
								sourceNode.name,
								incomingConnection.type,
								incomingConnection.outputIndex,
							);

							if (nodeIncomingData) {
								runIndex = nodeIncomingData.runIndex;
								incomingData.push(nodeIncomingData.data);
							}
						}

						incomingSourceData.main.push({
							previousNode: incomingConnection.from.name,
							previousNodeOutput: incomingConnection.outputIndex,
							previousNodeRun: runIndex,
						});
					}

					const executeData: IExecuteData = {
						node: startNode,
						data: { main: incomingData },
						source: incomingSourceData,
					};

					nodeExecutionStack.push(executeData);
				} else {
					const nodeName = startNode.name;
					const nextRunIndex = waitingExecution[nodeName]
						? Object.keys(waitingExecution[nodeName]).length
						: 0;

					for (const incomingConnection of sourceData.connections) {
						const sourceNode = incomingConnection.from;
						const maybeNodeIncomingData = getIncomingDataFromAnyRun(
							runData,
							sourceNode.name,
							incomingConnection.type,
							incomingConnection.outputIndex,
						);
						const nodeIncomingData = maybeNodeIncomingData?.data ?? null;

						if (nodeIncomingData) {
							addWaitingExecution(
								waitingExecution,
								nodeName,
								nextRunIndex,
								incomingConnection.type,
								incomingConnection.inputIndex,
								nodeIncomingData,
							);

							addWaitingExecutionSource(
								waitingExecutionSource,
								nodeName,
								nextRunIndex,
								incomingConnection.type,
								incomingConnection.inputIndex,
								nodeIncomingData
									? {
											previousNode: incomingConnection.from.name,
											previousNodeRun: nextRunIndex,
											previousNodeOutput: incomingConnection.outputIndex,
										}
									: null,
							);
						}
					}
				}
			}
		}
	}

	return {
		nodeExecutionStack,
		waitingExecution,
		waitingExecutionSource,
	};
}
