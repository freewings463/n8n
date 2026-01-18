"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/types/scenario.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/benchmark/src/types 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:ScenarioData、ScenarioManifest、Scenario。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Benchmark orchestration logic -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/types/scenario.ts -> services/n8n/application/n8n-benchmark/services/types/scenario.py

export type ScenarioData = {
	/** Relative paths to the workflow files */
	workflowFiles?: string[];
	/** Relative paths to the credential files */
	credentialFiles?: string[];
	/** Relative paths to the data table files */
	dataTableFile?: string;
};

/**
 * Configuration that defines the benchmark scenario
 */
export type ScenarioManifest = {
	/** The name of the scenario */
	name: string;
	/** A longer description of the scenario */
	description: string;
	/** Relative path to the k6 script */
	scriptPath: string;
	/** Data to import before running the scenario */
	scenarioData: ScenarioData;
};

/**
 * Scenario with additional metadata
 */
export type Scenario = ScenarioManifest & {
	id: string;
	/** Path to the directory containing the scenario */
	scenarioDirPath: string;
	/** ID of the data table created for the scenario, if any */
	dataTableId?: string;
};
