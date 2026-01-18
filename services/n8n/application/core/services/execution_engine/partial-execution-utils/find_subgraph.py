"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/partial-execution-utils/find-subgraph.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/partial-execution-utils 的执行模块。导入/依赖:外部:无；内部:n8n-workflow；本地:./directed-graph。导出:findSubgraph。关键函数/方法:findSubgraphRecursive、findSubgraph。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/partial-execution-utils/find-subgraph.ts -> services/n8n/application/core/services/execution_engine/partial-execution-utils/find_subgraph.py

import { NodeConnectionTypes, type INode } from 'n8n-workflow';

import type { GraphConnection } from './directed-graph';
import { DirectedGraph } from './directed-graph';

function findSubgraphRecursive(
	graph: DirectedGraph,
	destinationNode: INode,
	current: INode,
	trigger: INode,
	newGraph: DirectedGraph,
	currentBranch: GraphConnection[],
) {
	// If the current node is the chosen trigger keep this branch.
	if (current === trigger) {
		// If this graph consists of only one node there won't be any connections
		// and the loop below won't add anything.
		// We're adding the trigger here so that graphs with one node and no
		// connections are handled correctly.
		newGraph.addNode(trigger);

		for (const connection of currentBranch) {
			newGraph.addNodes(connection.from, connection.to);
			newGraph.addConnection(connection);
		}

		return;
	}

	const parentConnections = graph.getDirectParentConnections(current);

	// If the current node has no parents, don’t keep this branch.
	if (parentConnections.length === 0) {
		return;
	}

	// If the current node is the destination node again, don’t keep this branch.
	const isCycleWithDestinationNode =
		current === destinationNode && currentBranch.some((c) => c.to === destinationNode);
	if (isCycleWithDestinationNode) {
		return;
	}

	// If the current node was already visited, keep this branch.
	const isCycleWithCurrentNode = currentBranch.some((c) => c.to === current);
	if (isCycleWithCurrentNode) {
		// TODO: write function that adds nodes when adding connections
		for (const connection of currentBranch) {
			newGraph.addNodes(connection.from, connection.to);
			newGraph.addConnection(connection);
		}
		return;
	}

	// Recurse on each parent.
	for (const parentConnection of parentConnections) {
		// Skip parents that are connected via non-Main connection types. They are
		// only utility nodes for AI and are not part of the data or control flow
		// and can never lead too the trigger.
		if (parentConnection.type !== NodeConnectionTypes.Main) {
			continue;
		}

		findSubgraphRecursive(graph, destinationNode, parentConnection.from, trigger, newGraph, [
			...currentBranch,
			parentConnection,
		]);
	}
}

/**
 * Find all nodes that can lead from the trigger to the destination node.
 *
 * The algorithm is:
 *   Start with Destination Node
 *
 *   1. if the current node is the chosen trigger keep this branch
 *   2. if the current node has no parents, don’t keep this branch
 *   3. if the current node is the destination node again, don’t keep this
 *      branch
 *   4. if the current node was already visited, keep this branch
 *   5. Recurse on each parent
 *   6. Re-add all connections that don't use the `Main` connections type.
 *      Theses are used by nodes called root nodes and they are not part of the
 *      dataflow in the graph they are utility nodes, like the AI model used in a
 *      lang chain node.
 */
export function findSubgraph(options: {
	graph: DirectedGraph;
	destination: INode;
	trigger: INode;
}): DirectedGraph {
	const graph = options.graph;
	const destination = options.destination;
	const trigger = options.trigger;
	const subgraph = new DirectedGraph();

	findSubgraphRecursive(graph, destination, destination, trigger, subgraph, []);

	// For each node in the subgraph, if it has parent connections of a type that
	// is not `Main` in the input graph, add the connections and the nodes
	// connected to it to the subgraph
	//
	// Without this all AI related workflows would not work when executed
	// partially, because all utility nodes would be missing.
	for (const node of subgraph.getNodes().values()) {
		const parentConnections = graph.getParentConnections(node);

		for (const connection of parentConnections) {
			if (connection.type === NodeConnectionTypes.Main) {
				continue;
			}

			subgraph.addNodes(connection.from, connection.to);
			subgraph.addConnection(connection);
		}
	}

	return subgraph;
}
