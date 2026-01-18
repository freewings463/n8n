"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/utils/copy-input-items.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context/utils 的执行工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:copyInputItems。关键函数/方法:copyInputItems。用于提供执行通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/utils/copy-input-items.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/utils/copy_input_items.py

import type { INodeExecutionData, IDataObject } from 'n8n-workflow';
import { deepCopy } from 'n8n-workflow';

/**
 * Returns a copy of the items which only contains the json data and
 * of that only the defined properties
 */
export function copyInputItems(items: INodeExecutionData[], properties: string[]): IDataObject[] {
	return items.map((item) => {
		const newItem: IDataObject = {};
		for (const property of properties) {
			if (item.json[property] === undefined) {
				newItem[property] = null;
			} else {
				newItem[property] = deepCopy(item.json[property]);
			}
		}
		return newItem;
	});
}
