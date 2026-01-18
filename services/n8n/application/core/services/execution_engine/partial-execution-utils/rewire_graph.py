"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/partial-execution-utils/rewire-graph.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/partial-execution-utils 的执行模块。导入/依赖:外部:assert/strict；内部:@n8n/constants、n8n-workflow；本地:./directed-graph。导出:rewireGraph。关键函数/方法:rewireGraph。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/partial-execution-utils/rewire-graph.ts -> services/n8n/application/core/services/execution_engine/partial-execution-utils/rewire_graph.py

import { TOOL_EXECUTOR_NODE_NAME } from '@n8n/constants';
import * as a from 'assert/strict';
import { type AiAgentRequest, type INode, NodeConnectionTypes } from 'n8n-workflow';

import { type DirectedGraph } from './directed-graph';

export function rewireGraph(
	tool: INode,
	graph: DirectedGraph,
	agentRequest?: AiAgentRequest,
): DirectedGraph {
	const modifiedGraph = graph.clone();
	const children = modifiedGraph.getChildren(tool);

	if (children.size === 0) {
		return graph;
	}

	const rootNode = [...children][children.size - 1];

	a.ok(rootNode);

	const allIncomingConnection = modifiedGraph
		.getDirectParentConnections(rootNode)
		.filter((cn) => cn.type === NodeConnectionTypes.Main);

	// Create virtual agent node
	const toolExecutor: INode = {
		name: TOOL_EXECUTOR_NODE_NAME,
		disabled: false,
		type: '@n8n/n8n-nodes-langchain.toolExecutor',
		parameters: {
			query: agentRequest?.query ?? {},
			toolName: agentRequest?.tool?.name ?? '',
		},
		id: rootNode.id,
		typeVersion: 0,
		position: [0, 0],
	};

	// Add virtual agent to graph
	modifiedGraph.addNode(toolExecutor);

	// Rewire tool output to virtual agent
	tool.rewireOutputLogTo = NodeConnectionTypes.AiTool;
	modifiedGraph.addConnection({ from: tool, to: toolExecutor, type: NodeConnectionTypes.AiTool });

	// Rewire all incoming connections to virtual agent
	for (const cn of allIncomingConnection) {
		modifiedGraph.addConnection({ from: cn.from, to: toolExecutor, type: cn.type });
	}

	// Remove original agent node
	modifiedGraph.removeNode(rootNode);

	return modifiedGraph;
}
