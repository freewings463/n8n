"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/commands/new/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/commands/new 的入口。导入/依赖:外部:@clack/prompts、@oclif/core、change-case、node:fs/promises；内部:无；本地:./prompts、./utils、../template/core、../template/templates 等6项。导出:New。关键函数/方法:run、intro、config、packageManager、runCommand、note、outro。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/commands/new/index.ts -> services/n8n/infrastructure/n8n-node-cli/container/commands/new/__init__.py

import { confirm, intro, isCancel, log, note, outro, spinner } from '@clack/prompts';
import { Args, Command, Flags } from '@oclif/core';
import { camelCase } from 'change-case';
import fs from 'node:fs/promises';
import path from 'node:path';

import { declarativeTemplatePrompt, nodeNamePrompt, nodeTypePrompt } from './prompts';
import { createIntro } from './utils';
import type { TemplateData, TemplateWithRun } from '../../template/core';
import { getTemplate, isTemplateName, isTemplateType, templates } from '../../template/templates';
import { ChildProcessError, runCommand } from '../../utils/child-process';
import { delayAtLeast, folderExists } from '../../utils/filesystem';
import { initGit, tryReadGitUser } from '../../utils/git';
import { detectPackageManager } from '../../utils/package-manager';
import { onCancel } from '../../utils/prompts';
import { validateNodeName } from '../../utils/validation';

export default class New extends Command {
	static override description = 'Create a starter community node in a new directory';
	static override examples = [
		'<%= config.bin %> <%= command.id %>',
		'<%= config.bin %> <%= command.id %> n8n-nodes-my-app --skip-install',
		'<%= config.bin %> <%= command.id %> n8n-nodes-my-app --force',
		'<%= config.bin %> <%= command.id %> n8n-nodes-my-app --template declarative/custom',
	];
	static override args = {
		name: Args.string({ name: 'Name' }),
	};
	static override flags = {
		force: Flags.boolean({
			char: 'f',
			description: 'Overwrite destination folder if it already exists',
		}),
		'skip-install': Flags.boolean({ description: 'Skip installing dependencies' }),
		template: Flags.string({
			options: ['declarative/github-issues', 'declarative/custom', 'programmatic/example'] as const,
		}),
	};

	async run(): Promise<void> {
		const { flags, args } = await this.parse(New);
		const [typeFlag, templateFlag] = flags.template?.split('/') ?? [];

		intro(await createIntro());

		const nodeName = args.name ?? (await nodeNamePrompt());
		const invalidNodeNameError = validateNodeName(nodeName);

		if (invalidNodeNameError) return onCancel(invalidNodeNameError);

		const destination = path.resolve(process.cwd(), nodeName);

		let overwrite = false;
		if (await folderExists(destination)) {
			if (!flags.force) {
				const shouldOverwrite = await confirm({
					message: `./${nodeName} already exists, do you want to overwrite?`,
				});
				if (isCancel(shouldOverwrite) || !shouldOverwrite) return onCancel();
			}

			overwrite = true;
		}

		const type = typeFlag ?? (await nodeTypePrompt());
		if (!isTemplateType(type)) {
			return onCancel(`Invalid template type: ${type}`);
		}

		let template: TemplateWithRun = templates.programmatic.example;
		if (templateFlag) {
			const name = camelCase(templateFlag);
			if (!isTemplateName(type, name)) {
				return onCancel(`Invalid template name: ${name} for type: ${type}`);
			}
			template = getTemplate(type, name);
		} else if (type === 'declarative') {
			const chosenTemplate = await declarativeTemplatePrompt();
			template = getTemplate('declarative', chosenTemplate) as TemplateWithRun;
		}

		const config = (await template.prompts?.()) ?? {};
		const packageManager = (await detectPackageManager()) ?? 'npm';
		const templateData: TemplateData = {
			destinationPath: destination,
			nodePackageName: nodeName,
			config,
			user: tryReadGitUser(),
			packageManager: {
				name: packageManager,
				installCommand: packageManager === 'npm' ? 'ci' : 'install',
			},
		};
		const copyingSpinner = spinner();
		copyingSpinner.start('Copying files');
		if (overwrite) {
			await fs.rm(destination, { recursive: true, force: true });
		}
		await delayAtLeast(template.run(templateData), 1000);
		copyingSpinner.stop('Files copied');

		const gitSpinner = spinner();
		gitSpinner.start('Initializing git repository');

		try {
			await initGit(destination);

			gitSpinner.stop('Git repository initialized');
		} catch (error: unknown) {
			if (error instanceof ChildProcessError) {
				gitSpinner.stop(
					`Could not initialize git repository: ${error.message}`,
					error.code ?? undefined,
				);
				process.exit(error.code ?? 1);
			} else {
				throw error;
			}
		}

		if (!flags['skip-install']) {
			const installingSpinner = spinner();
			installingSpinner.start('Installing dependencies');

			try {
				await delayAtLeast(
					runCommand(packageManager, ['install'], {
						cwd: destination,
						printOutput: ({ stdout, stderr }) => {
							log.error(stdout.concat(stderr).toString());
						},
					}),
					1000,
				);
			} catch (error: unknown) {
				if (error instanceof ChildProcessError) {
					installingSpinner.stop(
						`Could not install dependencies: ${error.message}`,
						error.code ?? undefined,
					);
					process.exit(error.code ?? 1);
				} else {
					throw error;
				}
			}

			installingSpinner.stop('Dependencies installed');
		}

		note(
			`cd ./${nodeName} && ${packageManager} run dev

📚 Documentation: https://docs.n8n.io/integrations/creating-nodes/build/${type}-style-node/
💬 Community: https://community.n8n.io`,
			'Next Steps',
		);

		outro(`Created ./${nodeName} ✨`);
	}
}
