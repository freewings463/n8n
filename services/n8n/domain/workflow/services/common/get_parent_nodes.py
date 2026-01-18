"""
MIGRATION-META:
  source_path: packages/workflow/src/common/get-parent-nodes.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/common 的工作流模块。导入/依赖:外部:无；内部:无；本地:./get-connected-nodes、../interfaces。导出:getParentNodes。关键函数/方法:getParentNodes。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/common/get-parent-nodes.ts -> services/n8n/domain/workflow/services/common/get_parent_nodes.py

import { getConnectedNodes } from './get-connected-nodes';
import { NodeConnectionTypes } from '../interfaces';
import type { IConnections, NodeConnectionType } from '../interfaces';

/**
 * Returns all the nodes before the given one
 *
 * @param {NodeConnectionType} [type='main']
 * @param {*} [depth=-1]
 */
export function getParentNodes(
	connectionsByDestinationNode: IConnections,
	nodeName: string,
	type: NodeConnectionType | 'ALL' | 'ALL_NON_MAIN' = NodeConnectionTypes.Main,
	depth = -1,
): string[] {
	return getConnectedNodes(connectionsByDestinationNode, nodeName, type, depth);
}
