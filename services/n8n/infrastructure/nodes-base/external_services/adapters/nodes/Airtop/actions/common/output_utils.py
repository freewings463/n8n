"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/common/output.utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../transport/types。导出:parseJsonIfPresent、cleanOutputForToolUse。关键函数/方法:parseJsonIfPresent、cleanOutputForToolUse、getOutput。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/common/output.utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/common/output_utils.py

import { NodeOperationError } from 'n8n-workflow';
import type { IExecuteFunctions, IDataObject } from 'n8n-workflow';

import type { IAirtopNodeExecutionData, IAirtopResponse } from '../../transport/types';

/**
 * Parse JSON when the 'Parse JSON Output' parameter is enabled
 * @param this - The execution context
 * @param index - The index of the node
 * @param response - The Airtop API response to parse
 * @returns The parsed output
 */
export function parseJsonIfPresent(
	this: IExecuteFunctions,
	index: number,
	response: IAirtopResponse,
): IAirtopResponse {
	const parseJsonOutput = this.getNodeParameter('additionalFields.parseJsonOutput', index, false);
	const outputJsonSchema = this.getNodeParameter(
		'additionalFields.outputSchema',
		index,
		'',
	) as string;

	if (!parseJsonOutput || !outputJsonSchema.startsWith('{')) {
		return response;
	}

	try {
		const output = JSON.parse(response.data?.modelResponse ?? '') as IDataObject;
		return {
			sessionId: response.sessionId,
			windowId: response.windowId,
			output,
		};
	} catch (error) {
		throw new NodeOperationError(this.getNode(), 'Output is not a valid JSON');
	}
}

/**
 * Clean up the output when used as a tool
 * @param output - The output to clean up
 * @returns The cleaned up output
 */
export function cleanOutputForToolUse(output: IAirtopNodeExecutionData[]) {
	const getOutput = (executionData: IAirtopNodeExecutionData) => {
		// Return error message
		if (executionData.json?.errors?.length) {
			const errorMessage = executionData.json?.errors[0].message as string;
			return {
				output: `Error: ${errorMessage}`,
			};
		}

		// Return output parsed from JSON
		if (executionData.json?.output) {
			return executionData.json?.output;
		}

		// Return model response
		if (executionData.json?.data?.modelResponse) {
			return {
				output: executionData.json?.data?.modelResponse,
			};
		}

		// Return everything else
		return {
			output: { ...(executionData.json?.data ?? {}) },
		};
	};

	return output.map((executionData) => ({
		...executionData,
		json: {
			...getOutput(executionData),
		},
	}));
}
