"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/utils/construct-execution-metadata.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context/utils 的执行工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:constructExecutionMetaData。关键函数/方法:constructExecutionMetaData。用于提供执行通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/utils/construct-execution-metadata.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/utils/construct_execution_metadata.py

import type { INodeExecutionData, IPairedItemData, NodeExecutionWithMetadata } from 'n8n-workflow';

/**
 * Takes generic input data and brings it into the new json, pairedItem format n8n uses.
 * @param {(IPairedItemData)} itemData
 * @param {(INodeExecutionData[])} inputData
 */
export function constructExecutionMetaData(
	inputData: INodeExecutionData[],
	options: { itemData: IPairedItemData | IPairedItemData[] },
): NodeExecutionWithMetadata[] {
	const { itemData } = options;
	return inputData.map((data: INodeExecutionData) => {
		const { json, ...rest } = data;
		return { json, pairedItem: itemData, ...rest } as NodeExecutionWithMetadata;
	});
}
