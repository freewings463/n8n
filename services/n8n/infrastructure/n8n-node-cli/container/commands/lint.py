"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/commands/lint.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/commands 的模块。导入/依赖:外部:@clack/prompts、@oclif/core、node:fs/promises、picocolors；内部:无；本地:../utils/child-process、../utils/command-suggestions、../utils/package、../utils/prompts 等1项。导出:Lint。关键函数/方法:run、intro、checkStrictMode、verifyEslintConfig、handleLintErrors、containsCloudOnlyErrors。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/commands/lint.ts -> services/n8n/infrastructure/n8n-node-cli/container/commands/lint.py

import { intro } from '@clack/prompts';
import { Command, Flags } from '@oclif/core';
import fs from 'node:fs/promises';
import path from 'node:path';
import picocolors from 'picocolors';

import { ChildProcessError, runCommand } from '../utils/child-process';
import { suggestCloudSupportCommand } from '../utils/command-suggestions';
import { getPackageJson } from '../utils/package';
import { ensureN8nPackage, getCommandHeader } from '../utils/prompts';
import { isEnoentError } from '../utils/validation';

export default class Lint extends Command {
	static override description =
		'Lint the node in the current directory. Includes auto-fixing. In strict mode, verifies eslint config is unchanged from default.';
	static override examples = ['<%= config.bin %> <%= command.id %>'];
	static override flags = {
		fix: Flags.boolean({ description: 'Automatically fix problems', default: false }),
	};

	async run(): Promise<void> {
		const { flags } = await this.parse(Lint);

		intro(await getCommandHeader('n8n-node lint'));

		await ensureN8nPackage('lint');

		await this.checkStrictMode();

		const args = ['.'];

		if (flags.fix) {
			args.push('--fix');
		}

		let eslintOutput = '';
		try {
			await runCommand('eslint', args, {
				context: 'local',
				stdio: 'pipe',
				env: { ...process.env, FORCE_COLOR: '1' },
				alwaysPrintOutput: true,
				printOutput: ({ stdout, stderr }) => {
					eslintOutput = Buffer.concat([...stdout, ...stderr]).toString();
					process.stdout.write(Buffer.concat(stdout));
					process.stderr.write(Buffer.concat(stderr));
				},
			});
		} catch (error: unknown) {
			if (error instanceof ChildProcessError) {
				// Check if error might be related to cloud-only rules
				await this.handleLintErrors(eslintOutput);

				if (error.signal) {
					process.kill(process.pid, error.signal);
				} else {
					process.exit(error.code ?? 0);
				}
			}
			throw error;
		}
	}

	private async checkStrictMode(): Promise<void> {
		try {
			const workingDir = process.cwd();
			const packageJson = await getPackageJson(workingDir);
			if (!packageJson?.n8n?.strict) {
				return;
			}

			await this.verifyEslintConfig(workingDir);
		} catch (error) {
			return;
		}
	}

	private async verifyEslintConfig(workingDir: string): Promise<void> {
		const eslintConfigPath = path.resolve(workingDir, 'eslint.config.mjs');

		const templatePath = path.resolve(
			__dirname,
			'../template/templates/shared/default/eslint.config.mjs',
		);
		const expectedConfig = await fs.readFile(templatePath, 'utf-8');

		try {
			const currentConfig = await fs.readFile(eslintConfigPath, 'utf-8');

			const normalizedCurrent = currentConfig.replace(/\s+/g, ' ').trim();
			const normalizedExpected = expectedConfig.replace(/\s+/g, ' ').trim();

			if (normalizedCurrent !== normalizedExpected) {
				const enableCommand = await suggestCloudSupportCommand('enable');

				this.log(`${picocolors.red('Strict mode violation:')} ${picocolors.cyan('eslint.config.mjs')} has been modified from the default configuration.

${picocolors.dim('Expected:')}
${picocolors.gray(expectedConfig)}

To restore default config: ${enableCommand}
To disable strict mode: set ${picocolors.yellow('"strict": false')} in ${picocolors.cyan('package.json')} under the ${picocolors.yellow('"n8n"')} section.`);
				process.exit(1);
			}
		} catch (error: unknown) {
			if (isEnoentError(error)) {
				const enableCommand = await suggestCloudSupportCommand('enable');

				this.log(
					`${picocolors.red('Strict mode violation:')} ${picocolors.cyan('eslint.config.mjs')} not found. Expected default configuration.

To create default config: ${enableCommand}`,
				);
				process.exit(1);
			}
			throw error;
		}
	}

	private async handleLintErrors(eslintOutput: string): Promise<void> {
		if (this.containsCloudOnlyErrors(eslintOutput)) {
			const disableCommand = await suggestCloudSupportCommand('disable');

			this.log(`${picocolors.yellow('⚠️  n8n Cloud compatibility issues detected')}

These lint failures prevent verification to n8n Cloud.

To disable cloud compatibility checks:
  ${disableCommand}

${picocolors.dim(`Note: This will switch to ${picocolors.magenta('configWithoutCloudSupport')} and disable strict mode`)}`);
		}
	}

	private containsCloudOnlyErrors(errorMessage: string): boolean {
		const cloudOnlyRules = [
			'@n8n/community-nodes/no-restricted-imports',
			'@n8n/community-nodes/no-restricted-globals',
		];

		return cloudOnlyRules.some((rule) => errorMessage.includes(rule));
	}
}
