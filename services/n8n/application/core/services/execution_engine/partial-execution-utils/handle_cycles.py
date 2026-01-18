"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/partial-execution-utils/handle-cycles.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/partial-execution-utils 的执行模块。导入/依赖:外部:node:assert/strict；内部:n8n-workflow；本地:./directed-graph。导出:handleCycles。关键函数/方法:handleCycles。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/partial-execution-utils/handle-cycles.ts -> services/n8n/application/core/services/execution_engine/partial-execution-utils/handle_cycles.py

import type { INode } from 'n8n-workflow';
import * as a from 'node:assert/strict';

import type { DirectedGraph } from './directed-graph';

/**
 * Returns a new set of start nodes.
 *
 * For every start node this checks if it is part of a cycle and if it is it
 * replaces the start node with the start of the cycle.
 *
 * This is useful because it prevents executing cycles partially, e.g. figuring
 * our which run of the cycle has to be repeated etc.
 */
export function handleCycles(
	graph: DirectedGraph,
	startNodes: Set<INode>,
	trigger: INode,
): Set<INode> {
	// Strongly connected components can also be nodes that are not part of a
	// cycle. They form a strongly connected component of one. E.g the trigger is
	// always a strongly connected component by itself because it does not have
	// any inputs and thus cannot build a cycle.
	//
	// We're not interested in them so we filter them out.
	const cycles = graph.getStronglyConnectedComponents().filter((cycle) => cycle.size >= 1);
	const newStartNodes: Set<INode> = new Set(startNodes);

	// For each start node, check if the node is part of a cycle and if it is
	// replace the start node with the start of the cycle.
	if (cycles.length === 0) {
		return newStartNodes;
	}

	for (const startNode of startNodes) {
		for (const cycle of cycles) {
			const isPartOfCycle = cycle.has(startNode);
			if (isPartOfCycle) {
				const firstNode = graph.depthFirstSearch({
					from: trigger,
					fn: (node) => cycle.has(node),
				});

				a.ok(
					firstNode,
					"the trigger must be connected to the cycle, otherwise the cycle wouldn't be part of the subgraph",
				);

				newStartNodes.delete(startNode);
				newStartNodes.add(firstNode);
			}
		}
	}

	return newStartNodes;
}
