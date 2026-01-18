"""
MIGRATION-META:
  source_path: packages/cli/src/evaluation.ee/test-runner/utils.ee.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/evaluation.ee/test-runner 的模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:checkNodeParameterNotEmpty、extractTokenUsage。关键函数/方法:isRlcValue、checkNodeParameterNotEmpty、extractTokenUsage、extractFromNode、isValidTokenInfo。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/evaluation.ee/test-runner/utils.ee.ts -> services/n8n/application/cli/services/evaluation.ee/test-runner/utils_ee.py

import type {
	NodeParameterValueType,
	INodeParameterResourceLocator,
	IRunData,
	INodeExecutionData,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

type TokenUsageValues = {
	completionTokens: number;
	promptTokens: number;
	totalTokens: number;
};

type TokenUsageInfo = Record<`${string}__${number}` | 'total', TokenUsageValues>;

function isRlcValue(value: NodeParameterValueType): value is INodeParameterResourceLocator {
	return Boolean(
		typeof value === 'object' && value && 'value' in value && '__rl' in value && value.__rl,
	);
}

export function checkNodeParameterNotEmpty(value: NodeParameterValueType) {
	if (value === undefined || value === null || value === '') {
		return false;
	}

	if (isRlcValue(value)) {
		return checkNodeParameterNotEmpty(value.value);
	}

	return true;
}

export function extractTokenUsage(executionRunData: IRunData) {
	const result: TokenUsageInfo = {
		total: {
			completionTokens: 0,
			promptTokens: 0,
			totalTokens: 0,
		},
	};

	const extractFromNode = (nodeName: string, nodeData: INodeExecutionData, index: number) => {
		function isValidTokenInfo(data: unknown): data is TokenUsageValues {
			return (
				typeof data === 'object' &&
				data !== null &&
				'completionTokens' in data &&
				'promptTokens' in data &&
				'totalTokens' in data &&
				typeof data.completionTokens === 'number' &&
				typeof data.promptTokens === 'number' &&
				typeof data.totalTokens === 'number'
			);
		}

		const tokenInfo = nodeData.json?.tokenUsage ?? nodeData.json?.tokenUsageEstimate;

		if (tokenInfo && isValidTokenInfo(tokenInfo)) {
			result[`${nodeName}__${index}`] = {
				completionTokens: tokenInfo.completionTokens,
				promptTokens: tokenInfo.promptTokens,
				totalTokens: tokenInfo.totalTokens,
			};

			result.total.completionTokens += tokenInfo.completionTokens;
			result.total.promptTokens += tokenInfo.promptTokens;
			result.total.totalTokens += tokenInfo.totalTokens;
		}
	};

	for (const [nodeName, nodeData] of Object.entries(executionRunData)) {
		if (nodeData[0]?.data?.[NodeConnectionTypes.AiLanguageModel]) {
			for (const [index, node] of nodeData.entries()) {
				const modelNodeExecutionData = node.data?.[NodeConnectionTypes.AiLanguageModel]?.[0]?.[0];
				if (modelNodeExecutionData) {
					extractFromNode(nodeName, modelNodeExecutionData, index);
				}
			}
		}
	}

	return result;
}
