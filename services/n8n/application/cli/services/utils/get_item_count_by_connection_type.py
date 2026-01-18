"""
MIGRATION-META:
  source_path: packages/cli/src/utils/get-item-count-by-connection-type.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/utils 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:getItemCountByConnectionType。关键函数/方法:getItemCountByConnectionType。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/utils/get-item-count-by-connection-type.ts -> services/n8n/application/cli/services/utils/get_item_count_by_connection_type.py

import type { NodeConnectionType, ITaskData } from 'n8n-workflow';
import { isNodeConnectionType } from 'n8n-workflow';

export function getItemCountByConnectionType(
	data: ITaskData['data'],
): Partial<Record<NodeConnectionType, number[]>> {
	const itemCountByConnectionType: Partial<Record<NodeConnectionType, number[]>> = {};

	for (const [connectionType, connectionData] of Object.entries(data ?? {})) {
		if (!isNodeConnectionType(connectionType)) {
			continue;
		}

		if (Array.isArray(connectionData)) {
			itemCountByConnectionType[connectionType] = connectionData.map((d) => (d ? d.length : 0));
		} else {
			itemCountByConnectionType[connectionType] = [0];
		}
	}

	return itemCountByConnectionType;
}
