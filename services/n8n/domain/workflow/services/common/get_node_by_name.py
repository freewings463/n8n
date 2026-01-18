"""
MIGRATION-META:
  source_path: packages/workflow/src/common/get-node-by-name.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/common 的工作流模块。导入/依赖:外部:无；内部:无；本地:../interfaces。导出:getNodeByName。关键函数/方法:getNodeByName。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/common/get-node-by-name.ts -> services/n8n/domain/workflow/services/common/get_node_by_name.py

import type { INode, INodes } from '../interfaces';

/**
 * Returns the node with the given name if it exists else null
 *
 * @param {INodes} nodes Nodes to search in
 * @param {string} name Name of the node to return
 */
export function getNodeByName(nodes: INodes | INode[], name: string) {
	if (Array.isArray(nodes)) {
		return nodes.find((node) => node.name === name) || null;
	}

	if (nodes.hasOwnProperty(name)) {
		return nodes[name];
	}

	return null;
}
