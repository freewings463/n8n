"""
MIGRATION-META:
  source_path: packages/workflow/src/common/map-connections-by-destination.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/common 的工作流模块。导入/依赖:外部:无；内部:无；本地:../interfaces。导出:mapConnectionsByDestination。关键函数/方法:mapConnectionsByDestination。用于承载工作流实现细节，并通过导出对外提供能力。注释目标:eslint-disable @typescript-eslint/no-for-in-array。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/common/map-connections-by-destination.ts -> services/n8n/domain/workflow/services/common/map_connections_by_destination.py

/* eslint-disable @typescript-eslint/no-for-in-array */

import type { IConnections, NodeConnectionType } from '../interfaces';

export function mapConnectionsByDestination(connections: IConnections) {
	const returnConnection: IConnections = {};

	let connectionInfo;
	let maxIndex: number;
	for (const sourceNode in connections) {
		if (!connections.hasOwnProperty(sourceNode)) {
			continue;
		}

		for (const type of Object.keys(connections[sourceNode]) as NodeConnectionType[]) {
			if (!connections[sourceNode].hasOwnProperty(type)) {
				continue;
			}

			for (const inputIndex in connections[sourceNode][type]) {
				if (!connections[sourceNode][type].hasOwnProperty(inputIndex)) {
					continue;
				}

				for (connectionInfo of connections[sourceNode][type][inputIndex] ?? []) {
					if (!returnConnection.hasOwnProperty(connectionInfo.node)) {
						returnConnection[connectionInfo.node] = {};
					}
					if (!returnConnection[connectionInfo.node].hasOwnProperty(connectionInfo.type)) {
						returnConnection[connectionInfo.node][connectionInfo.type] = [];
					}

					maxIndex = returnConnection[connectionInfo.node][connectionInfo.type].length - 1;
					for (let j = maxIndex; j < connectionInfo.index; j++) {
						returnConnection[connectionInfo.node][connectionInfo.type].push([]);
					}

					returnConnection[connectionInfo.node][connectionInfo.type][connectionInfo.index]?.push({
						node: sourceNode,
						type,
						index: parseInt(inputIndex, 10),
					});
				}
			}
		}
	}

	return returnConnection;
}
