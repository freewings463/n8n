"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/commands/list.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/benchmark/src/commands 的模块。导入/依赖:外部:@oclif/core；内部:@/config/common-flags、@/scenario/scenario-loader；本地:无。导出:ListCommand。关键函数/方法:run。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Benchmark orchestration logic -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/commands/list.ts -> services/n8n/application/n8n-benchmark/services/commands/list.py

import { Command } from '@oclif/core';

import { testScenariosPath } from '@/config/common-flags';
import { ScenarioLoader } from '@/scenario/scenario-loader';

export default class ListCommand extends Command {
	static description = 'List all available scenarios';

	static flags = {
		testScenariosPath,
	};

	async run() {
		const { flags } = await this.parse(ListCommand);
		const scenarioLoader = new ScenarioLoader();

		const allScenarios = scenarioLoader.loadAll(flags.testScenariosPath);

		console.log('Available test scenarios:');
		console.log('');

		for (const scenario of allScenarios) {
			console.log('\t', scenario.name, ':', scenario.description);
		}
	}
}
