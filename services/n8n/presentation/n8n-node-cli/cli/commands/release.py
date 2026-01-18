"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/commands/release.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/node-cli/src/commands 的模块。导入/依赖:外部:@clack/prompts、@oclif/core；内部:无；本地:../utils/child-process、../utils/package-manager、../utils/prompts。导出:Release。关键函数/方法:run、intro、pm。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI package default -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/commands/release.ts -> services/n8n/presentation/n8n-node-cli/cli/commands/release.py

import { intro } from '@clack/prompts';
import { Command } from '@oclif/core';

import { ChildProcessError, runCommand } from '../utils/child-process';
import { detectPackageManager } from '../utils/package-manager';
import { getCommandHeader } from '../utils/prompts';

export default class Release extends Command {
	static override description = 'Publish your community node package to npm';
	static override examples = ['<%= config.bin %> <%= command.id %>'];
	static override flags = {};

	async run(): Promise<void> {
		await this.parse(Release);

		intro(await getCommandHeader('n8n-node release'));

		const pm = (await detectPackageManager()) ?? 'npm';

		try {
			await runCommand(
				'release-it',
				[
					'-n',
					'--git.requireBranch main',
					'--git.requireCleanWorkingDir',
					'--git.requireUpstream',
					'--git.requireCommits',
					'--git.commit',
					'--git.tag',
					'--git.push',
					'--git.changelog="npx auto-changelog --stdout --unreleased --commit-limit false -u --hide-credit"',
					'--github.release',
					`--hooks.before:init="${pm} run lint && ${pm} run build"`,
					'--hooks.after:bump="npx auto-changelog -p"',
				],
				{
					stdio: 'inherit',
					context: 'local',
					env: {
						RELEASE_MODE: 'true',
					},
				},
			);
		} catch (error) {
			if (error instanceof ChildProcessError) {
				if (error.signal) {
					process.kill(process.pid, error.signal);
				} else {
					process.exit(error.code ?? 0);
				}
			}
			throw error;
		}
	}
}
