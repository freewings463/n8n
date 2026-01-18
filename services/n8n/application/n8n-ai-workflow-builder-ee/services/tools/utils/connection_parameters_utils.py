"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/utils/connection-parameters.utils.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools/utils 的工作流工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:CONNECTION_AFFECTING_PARAMETERS、validateConnectionParameters、extractConnectionParameters。关键函数/方法:validateConnectionParameters、extractConnectionParameters。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/utils/connection-parameters.utils.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/tools/utils/connection_parameters_utils.py

import type { INodeParameters } from 'n8n-workflow';

/**
 * Whitelist of parameter names that commonly affect node connections
 * These parameters often control which inputs/outputs are available
 */
export const CONNECTION_AFFECTING_PARAMETERS = new Set([
	'mode',
	'operation',
	'resource',
	'action',
	'method',
	'textSplittingMode',
	'useReranker',
	'outputFormat',
	'inputType',
	'outputType',
	'connectionMode',
	'dataType',
	'triggerMode',
]);

/**
 * Validate that the provided parameters only contain connection-affecting parameters
 * @param parameters - The parameters to validate
 * @returns Object with validation result and filtered parameters
 */
export function validateConnectionParameters(parameters: INodeParameters): {
	valid: boolean;
	filtered: INodeParameters;
	warnings: string[];
} {
	const filtered: INodeParameters = {};
	const warnings: string[] = [];

	for (const [key, value] of Object.entries(parameters)) {
		if (CONNECTION_AFFECTING_PARAMETERS.has(key)) {
			filtered[key] = value;
		} else {
			warnings.push(
				`Parameter "${key}" is not a connection-affecting parameter and will be ignored`,
			);
		}
	}

	return {
		valid: Object.keys(filtered).length > 0,
		filtered,
		warnings,
	};
}

/**
 * Extract only connection-affecting parameters from a node's current parameters
 * @param parameters - The node's full parameters
 * @returns Only the connection-affecting parameters
 */
export function extractConnectionParameters(parameters: INodeParameters): INodeParameters {
	const connectionParams: INodeParameters = {};

	for (const [key, value] of Object.entries(parameters)) {
		if (CONNECTION_AFFECTING_PARAMETERS.has(key)) {
			connectionParams[key] = value;
		}
	}

	return connectionParams;
}
