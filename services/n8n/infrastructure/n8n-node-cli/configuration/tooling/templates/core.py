"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/core.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template 的模块。导入/依赖:外部:fast-glob、handlebars、node:fs/promises；内部:无；本地:../utils/filesystem。导出:TemplateData、Template、TemplateWithRun、createTemplate。关键函数/方法:copyDefaultTemplateFilesToDestination、templateStaticFiles。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/core.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/core.py

import glob from 'fast-glob';
import handlebars from 'handlebars';
import fs from 'node:fs/promises';
import path from 'node:path';

import { copyFolder } from '../utils/filesystem';

export type TemplateData<Config extends object = object> = {
	destinationPath: string;
	nodePackageName: string;
	user?: Partial<{
		name: string;
		email: string;
	}>;
	packageManager: {
		name: 'npm' | 'yarn' | 'pnpm';
		installCommand: string;
	};
	config: Config;
};

type Require<T, K extends keyof T> = T & { [P in K]-?: T[P] };
export type Template<Config extends object = object> = {
	name: string;
	description: string;
	path: string;
	prompts?: () => Promise<Config>;
	run?: (data: TemplateData<Config>) => Promise<void>;
};

export type TemplateWithRun<Config extends object = object> = Require<Template<Config>, 'run'>;

export async function copyTemplateFilesToDestination<Config extends object>(
	template: Template<Config>,
	data: TemplateData,
) {
	await copyFolder({
		source: template.path,
		destination: data.destinationPath,
		ignore: ['dist', 'node_modules'],
	});
}

export async function copyDefaultTemplateFilesToDestination(data: TemplateData) {
	await copyFolder({
		source: path.resolve(__dirname, 'templates/shared/default'),
		destination: data.destinationPath,
		ignore: ['dist', 'node_modules'],
	});
}

export async function templateStaticFiles(data: TemplateData) {
	const files = await glob('**/*.{md,json,yml}', {
		ignore: ['tsconfig.json', 'tsconfig.build.json'],
		cwd: data.destinationPath,
		absolute: true,
		dot: true,
	});

	await Promise.all(
		files.map(async (file) => {
			const content = await fs.readFile(file, 'utf-8');
			const newContent = handlebars.compile(content, { noEscape: true })(data);

			if (newContent !== content) {
				await fs.writeFile(file, newContent);
			}
		}),
	);
}

export function createTemplate<Config extends object>(
	template: Template<Config>,
): TemplateWithRun<Config> {
	return {
		...template,
		run: async (data) => {
			await copyDefaultTemplateFilesToDestination(data);
			await copyTemplateFilesToDestination(template, data);
			await templateStaticFiles(data);
			await template.run?.(data);
		},
	};
}
