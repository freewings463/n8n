"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/commands/build.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/commands 的模块。导入/依赖:外部:@clack/prompts、@oclif/core、fast-glob、node:fs/promises、rimraf；内部:无；本地:../utils/child-process、../utils/prompts。导出:Build。关键函数/方法:run、intro、cancel、outro、runTscBuild、copyStaticFiles。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/commands/build.ts -> services/n8n/infrastructure/n8n-node-cli/container/commands/build.py

import { cancel, intro, log, outro, spinner } from '@clack/prompts';
import { Command } from '@oclif/core';
import glob from 'fast-glob';
import { cp, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { rimraf } from 'rimraf';

import { runCommand } from '../utils/child-process';
import { ensureN8nPackage, getCommandHeader } from '../utils/prompts';

export default class Build extends Command {
	static override description = 'Compile the node in the current directory and copy assets';
	static override examples = ['<%= config.bin %> <%= command.id %>'];
	static override flags = {};

	async run(): Promise<void> {
		await this.parse(Build);

		const commandName = 'n8n-node build';
		intro(await getCommandHeader(commandName));

		await ensureN8nPackage(commandName);

		const buildSpinner = spinner();
		buildSpinner.start('Building TypeScript files');
		await rimraf('dist');

		try {
			await runTscBuild();
			buildSpinner.stop('TypeScript build successful');
		} catch (error) {
			cancel('TypeScript build failed');
			this.exit(1);
		}

		const copyStaticFilesSpinner = spinner();
		copyStaticFilesSpinner.start('Copying static files');
		await copyStaticFiles();
		copyStaticFilesSpinner.stop('Copied static files');

		outro('✓ Build successful');
	}
}

async function runTscBuild(): Promise<void> {
	return await runCommand('tsc', [], {
		context: 'local',
		printOutput: ({ stdout, stderr }) => {
			log.error(stdout.concat(stderr).toString());
		},
	});
}

export async function copyStaticFiles() {
	const staticFiles = glob.sync(['**/*.{png,svg}', '**/__schema__/**/*.json'], {
		ignore: ['dist', 'node_modules'],
	});

	return await Promise.all(
		staticFiles.map(async (filePath) => {
			const destPath = path.join('dist', filePath);
			await mkdir(path.dirname(destPath), { recursive: true });
			return await cp(filePath, destPath, { recursive: true });
		}),
	);
}
