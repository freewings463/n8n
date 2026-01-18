"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/utils/cleanup-parameter-data.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context/utils 的执行工具。导入/依赖:外部:luxon；内部:n8n-workflow；本地:无。导出:cleanupParameterData。关键函数/方法:cleanupParameterData、value。用于提供执行通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/utils/cleanup-parameter-data.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/utils/cleanup_parameter_data.py

import { DateTime } from 'luxon';
import type { INodeParameters, NodeParameterValueType } from 'n8n-workflow';

/**
 * Clean up parameter data to make sure that only valid data gets returned
 * INFO: Currently only converts Luxon Dates as we know for sure it will not be breaking
 */
export function cleanupParameterData(inputData: NodeParameterValueType): void {
	if (typeof inputData !== 'object' || inputData === null) {
		return;
	}

	if (Array.isArray(inputData)) {
		inputData.forEach((value) => cleanupParameterData(value as NodeParameterValueType));
		return;
	}

	if (typeof inputData === 'object') {
		Object.keys(inputData).forEach((key) => {
			const value = (inputData as INodeParameters)[key];
			if (typeof value === 'object') {
				if (DateTime.isDateTime(value)) {
					// Is a special luxon date so convert to string
					(inputData as INodeParameters)[key] = value.toString();
				} else {
					cleanupParameterData(value);
				}
			}
		});
	}
}
