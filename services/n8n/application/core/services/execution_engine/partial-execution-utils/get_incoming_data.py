"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/partial-execution-utils/get-incoming-data.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/partial-execution-utils 的执行模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:getIncomingData、getIncomingDataFromAnyRun。关键函数/方法:getIncomingData、getRunIndexLength、getIncomingDataFromAnyRun。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/partial-execution-utils/get-incoming-data.ts -> services/n8n/application/core/services/execution_engine/partial-execution-utils/get_incoming_data.py

import type { INodeExecutionData, IRunData, NodeConnectionType } from 'n8n-workflow';

export function getIncomingData(
	runData: IRunData,
	nodeName: string,
	runIndex: number,
	connectionType: NodeConnectionType,
	outputIndex: number,
): INodeExecutionData[] | null {
	return runData[nodeName]?.at(runIndex)?.data?.[connectionType].at(outputIndex) ?? null;
}

function getRunIndexLength(runData: IRunData, nodeName: string) {
	return runData[nodeName]?.length ?? 0;
}

export function getIncomingDataFromAnyRun(
	runData: IRunData,
	nodeName: string,
	connectionType: NodeConnectionType,
	outputIndex: number,
): { data: INodeExecutionData[]; runIndex: number } | undefined {
	const maxRunIndexes = getRunIndexLength(runData, nodeName);

	for (let runIndex = 0; runIndex < maxRunIndexes; runIndex++) {
		const data = getIncomingData(runData, nodeName, runIndex, connectionType, outputIndex);

		if (data && data.length > 0) {
			return { data, runIndex };
		}
	}

	return undefined;
}
