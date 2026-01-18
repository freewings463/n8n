"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/scenario/scenario-data-loader.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/src/scenario 的模块。导入/依赖:外部:无；内部:@/n8n-api-client/n8n-api-client.types、@/types/scenario；本地:无。导出:LoadableScenarioData、ScenarioDataFileLoader。关键函数/方法:loadDataForScenario、loadSingleCredentialFromFile、loadSingleWorkflowFromFile、loadSingleDataTableFromFile。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/scenario/scenario-data-loader.ts -> services/n8n/infrastructure/n8n-benchmark/container/scenario/scenario_data_loader.py

import * as fs from 'node:fs';
import * as path from 'node:path';

import type { Workflow, Credential, DataTable } from '@/n8n-api-client/n8n-api-client.types';
import type { Scenario } from '@/types/scenario';

export type LoadableScenarioData = {
	workflows: Workflow[];
	credentials: Credential[];
	dataTable: DataTable | null;
};

/**
 * Loads scenario data files from FS
 */
export class ScenarioDataFileLoader {
	async loadDataForScenario(scenario: Scenario): Promise<LoadableScenarioData> {
		const workflows = await Promise.all(
			scenario.scenarioData.workflowFiles?.map((workflowFilePath) =>
				this.loadSingleWorkflowFromFile(path.join(scenario.scenarioDirPath, workflowFilePath)),
			) ?? [],
		);

		const credentials = await Promise.all(
			scenario.scenarioData.credentialFiles?.map((credentialFilePath) =>
				this.loadSingleCredentialFromFile(path.join(scenario.scenarioDirPath, credentialFilePath)),
			) ?? [],
		);

		const dataTable = scenario.scenarioData.dataTableFile
			? this.loadSingleDataTableFromFile(
					path.join(scenario.scenarioDirPath, scenario.scenarioData.dataTableFile),
				)
			: null;

		return {
			workflows,
			credentials,
			dataTable,
		};
	}

	private loadSingleCredentialFromFile(credentialFilePath: string): Credential {
		const fileContent = fs.readFileSync(credentialFilePath, 'utf8');

		try {
			return JSON.parse(fileContent) as Credential;
		} catch (error) {
			const e = error as Error;
			throw new Error(`Failed to parse credential file ${credentialFilePath}: ${e.message}`);
		}
	}

	private loadSingleWorkflowFromFile(workflowFilePath: string): Workflow {
		const fileContent = fs.readFileSync(workflowFilePath, 'utf8');

		try {
			return JSON.parse(fileContent) as Workflow;
		} catch (error) {
			const e = error as Error;
			throw new Error(`Failed to parse workflow file ${workflowFilePath}: ${e.message}`);
		}
	}

	private loadSingleDataTableFromFile(dataTableFilePath: string): DataTable {
		const fileContent = fs.readFileSync(dataTableFilePath, 'utf8');

		try {
			return JSON.parse(fileContent) as DataTable;
		} catch (error) {
			const e = error as Error;
			throw new Error(`Failed to parse data table file ${dataTableFilePath}: ${e.message}`);
		}
	}
}
