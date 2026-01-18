"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/commands/prerelease.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/node-cli/src/commands 的模块。导入/依赖:外部:@oclif/core；内部:无；本地:../utils/package-manager。导出:Prerelease。关键函数/方法:run、packageManager。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI package default -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/commands/prerelease.ts -> services/n8n/presentation/n8n-node-cli/cli/commands/prerelease.py

import { Command } from '@oclif/core';

import { detectPackageManager } from '../utils/package-manager';

export default class Prerelease extends Command {
	static override description =
		'Only for internal use. Prevent npm publish, instead require npm run release';
	static override examples = ['<%= config.bin %> <%= command.id %>'];
	static override flags = {};
	static override hidden = true;

	async run(): Promise<void> {
		await this.parse(Prerelease);

		const packageManager = (await detectPackageManager()) ?? 'npm';

		if (!process.env.RELEASE_MODE) {
			this.log(`Run \`${packageManager} run release\` to publish the package`);
			process.exit(1);
		}
	}
}
