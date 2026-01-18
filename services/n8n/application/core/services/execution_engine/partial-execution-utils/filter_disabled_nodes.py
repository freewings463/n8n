"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/partial-execution-utils/filter-disabled-nodes.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/partial-execution-utils 的执行模块。导入/依赖:外部:无；内部:n8n-workflow；本地:./directed-graph。导出:filterDisabledNodes。关键函数/方法:filterDisabledNodes。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/partial-execution-utils/filter-disabled-nodes.ts -> services/n8n/application/core/services/execution_engine/partial-execution-utils/filter_disabled_nodes.py

import { NodeConnectionTypes } from 'n8n-workflow';

import type { DirectedGraph } from './directed-graph';

export function filterDisabledNodes(graph: DirectedGraph): DirectedGraph {
	const filteredGraph = graph.clone();

	for (const node of filteredGraph.getNodes().values()) {
		if (node.disabled) {
			filteredGraph.removeNode(node, {
				reconnectConnections: true,
				skipConnectionFn: (c) => c.type !== NodeConnectionTypes.Main,
			});
		}
	}

	return filteredGraph;
}
