"""
MIGRATION-META:
  source_path: packages/node-dev/commands/build.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/node-dev/commands 的模块。导入/依赖:外部:@oclif/core；内部:@n8n/di、n8n-core；本地:../src。导出:Build。关键函数/方法:run。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-dev command -> presentation/cli/commands
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/node-dev/commands/build.ts -> services/n8n/presentation/node-dev/cli/commands/build.py

import { Container } from '@n8n/di';
import { Command, Flags } from '@oclif/core';
import { InstanceSettings } from 'n8n-core';

import type { IBuildOptions } from '../src';
import { buildFiles } from '../src';

export class Build extends Command {
	static description = 'Builds credentials and nodes and copies it to n8n custom extension folder';

	static examples = [
		'$ n8n-node-dev build',
		'$ n8n-node-dev build --destination ~/n8n-nodes',
		'$ n8n-node-dev build --watch',
	];

	static flags = {
		help: Flags.help({ char: 'h' }),
		destination: Flags.string({
			char: 'd',
			description: `The path to copy the compiled files to [default: ${
				Container.get(InstanceSettings).customExtensionDir
			}]`,
		}),
		watch: Flags.boolean({
			description:
				'Starts in watch mode and automatically builds and copies file whenever they change',
		}),
	};

	async run() {
		const { flags } = await this.parse(Build);

		this.log('\nBuild credentials and nodes');
		this.log('=========================');

		try {
			const options: IBuildOptions = {};

			if (flags.destination) {
				options.destinationFolder = flags.destination;
			}
			if (flags.watch) {
				options.watch = true;
			}

			const outputDirectory = await buildFiles(options);

			this.log(`The nodes got built and saved into the following folder:\n${outputDirectory}`);
		} catch (error) {
			// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
			this.log(`\nGOT ERROR: "${error.message}"`);
			this.log('====================================');
			// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-argument
			this.log(error.stack);
		}
	}
}
