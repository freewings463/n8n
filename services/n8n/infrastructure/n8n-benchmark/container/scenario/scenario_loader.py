"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/scenario/scenario-loader.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/src/scenario 的模块。导入/依赖:外部:无；内部:@/types/scenario；本地:无。导出:ScenarioLoader。关键函数/方法:loadAll、loadAndValidateScenarioManifest、loadScenarioManifest、formScenarioId。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/scenario/scenario-loader.ts -> services/n8n/infrastructure/n8n-benchmark/container/scenario/scenario_loader.py

import { createHash } from 'node:crypto';
import * as fs from 'node:fs';
import * as path from 'path';

import type { Scenario, ScenarioManifest } from '@/types/scenario';

export class ScenarioLoader {
	/**
	 * Loads all scenarios from the given path
	 */
	loadAll(pathToScenarios: string, filter?: string): Scenario[] {
		pathToScenarios = path.resolve(pathToScenarios);
		const scenarioFolders = fs
			.readdirSync(pathToScenarios, { withFileTypes: true })
			.filter((dirent) => dirent.isDirectory())
			.map((dirent) => dirent.name);

		const scenarios: Scenario[] = [];

		for (const folder of scenarioFolders) {
			if (filter && folder.toLowerCase() !== filter.toLowerCase()) {
				continue;
			}
			const scenarioPath = path.join(pathToScenarios, folder);
			const manifestFileName = `${folder}.manifest.json`;
			const scenarioManifestPath = path.join(pathToScenarios, folder, manifestFileName);
			if (!fs.existsSync(scenarioManifestPath)) {
				console.warn(`Scenario at ${scenarioPath} is missing the ${manifestFileName} file`);
				continue;
			}

			// Load the scenario manifest file
			const [scenario, validationErrors] =
				this.loadAndValidateScenarioManifest(scenarioManifestPath);
			if (validationErrors) {
				console.warn(
					`Scenario at ${scenarioPath} has the following validation errors: ${validationErrors.join(', ')}`,
				);
				continue;
			}

			scenarios.push({
				...scenario,
				id: this.formScenarioId(scenarioPath),
				scenarioDirPath: scenarioPath,
			});
		}

		return scenarios;
	}

	private loadAndValidateScenarioManifest(
		scenarioManifestPath: string,
	): [ScenarioManifest, null] | [null, string[]] {
		const [scenario, error] = this.loadScenarioManifest(scenarioManifestPath);
		if (!scenario) {
			return [null, [error]];
		}

		const validationErrors: string[] = [];

		if (!scenario.name) {
			validationErrors.push(`Scenario at ${scenarioManifestPath} is missing a name`);
		}
		if (!scenario.description) {
			validationErrors.push(`Scenario at ${scenarioManifestPath} is missing a description`);
		}

		return validationErrors.length === 0 ? [scenario, null] : [null, validationErrors];
	}

	private loadScenarioManifest(
		scenarioManifestPath: string,
	): [ScenarioManifest, null] | [null, string] {
		try {
			const scenario = JSON.parse(
				fs.readFileSync(scenarioManifestPath, 'utf8'),
			) as ScenarioManifest;

			return [scenario, null];
		} catch (error) {
			const message = error instanceof Error ? error.message : JSON.stringify(error);
			return [null, `Failed to parse manifest ${scenarioManifestPath}: ${message}`];
		}
	}

	private formScenarioId(scenarioPath: string): string {
		return createHash('sha256').update(scenarioPath).digest('hex');
	}
}
