"""
MIGRATION-META:
  source_path: packages/workflow/src/run-execution-data/run-execution-data.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/run-execution-data 的工作流模块。导入/依赖:外部:无；内部:无；本地:./run-execution-data.v0、./run-execution-data.v1。导出:IRunExecutionDataAll、IRunExecutionData、migrateRunExecutionData。关键函数/方法:migrateRunExecutionData。用于承载工作流实现细节，并通过导出对外提供能力。注释目标:Contains all the data which is needed to execute a workflow and so also to / restart it again if it fails.。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/run-execution-data/run-execution-data.ts -> services/n8n/domain/workflow/services/run-execution-data/run_execution_data.py

/**
 * Contains all the data which is needed to execute a workflow and so also to
 * restart it again if it fails.
 * RunData, ExecuteData and WaitForExecution contain often the same data.
 *
 */

import type { IRunExecutionDataV0 } from './run-execution-data.v0';
import { runExecutionDataV0ToV1, type IRunExecutionDataV1 } from './run-execution-data.v1';

/**
 * All the versions of the interface.
 * !!! Only used at the data access layer to handle records saved under older versions. !!!
 * !!! All other code should use the current version, below. !!!
 */
export type IRunExecutionDataAll = IRunExecutionDataV0 | IRunExecutionDataV1;

const __brand = Symbol('brand');

/**
 * Current version of IRunExecutionData.
 */
export type IRunExecutionData = IRunExecutionDataV1 & {
	[__brand]: 'Use createRunExecutionData factory instead of constructing manually';
};

export function migrateRunExecutionData(data: IRunExecutionDataAll): IRunExecutionData {
	switch (data.version) {
		case 0:
		case undefined: // Missing version means version 0
			data = runExecutionDataV0ToV1(data);
		// Fall through to subsequent versions as they're added.
	}

	if (data.version !== 1) {
		throw new Error(
			`Unsupported IRunExecutionData version: ${(data as { version?: number }).version}`,
		);
	}

	return data as IRunExecutionData;
}
