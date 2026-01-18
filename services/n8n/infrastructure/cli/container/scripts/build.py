"""
MIGRATION-META:
  source_path: packages/cli/scripts/build.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/scripts 的模块。导入/依赖:外部:shelljs、@vvo/tzdb、fast-glob；内部:无；本地:无。导出:无。关键函数/方法:generateUserManagementEmailTemplates、generateTimezoneData、createPublicApiDirectory、copySwaggerTheme、bundleOpenApiSpecs、mkdirSync、writeFileSync。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/scripts/build.mjs -> services/n8n/infrastructure/cli/container/scripts/build.py

import path from 'path';
import { writeFileSync, existsSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import shell from 'shelljs';
import { rawTimeZones } from '@vvo/tzdb';
import glob from 'fast-glob';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT_DIR = path.resolve(__dirname, '..');
const SPEC_FILENAME = 'openapi.yml';
const SPEC_THEME_FILENAME = 'swagger-theme.css';

const publicApiEnabled = process.env.N8N_PUBLIC_API_DISABLED !== 'true';

generateUserManagementEmailTemplates();
generateTimezoneData();

if (publicApiEnabled) {
	createPublicApiDirectory();
	copySwaggerTheme();
	bundleOpenApiSpecs();
}

function generateUserManagementEmailTemplates() {
	const sourceDir = path.resolve(ROOT_DIR, 'src', 'user-management', 'email', 'templates');
	const destinationDir = path.resolve(ROOT_DIR, 'dist', 'user-management', 'email', 'templates');

	shell.mkdir('-p', destinationDir);

	const templates = glob.sync('*.mjml', { cwd: sourceDir });
	templates.forEach((template) => {
		if (template.startsWith('_')) return;
		const source = path.resolve(sourceDir, template);
		const destination = path.resolve(destinationDir, template.replace(/\.mjml$/, '.handlebars'));
		const command = `pnpm mjml --output "${destination}" "${source}"`;
		shell.exec(command, { silent: false });
	});

	shell.cp(path.resolve(sourceDir, 'n8n-logo.png'), destinationDir);
}

function createPublicApiDirectory() {
	const publicApiDirectory = path.resolve(ROOT_DIR, 'dist', 'public-api', 'v1');
	if (!existsSync(publicApiDirectory)) {
		console.log('Creating directory', publicApiDirectory);
		mkdirSync(publicApiDirectory, { recursive: true });
	}
}

function copySwaggerTheme() {
	const swaggerTheme = {
		source: path.resolve(ROOT_DIR, 'src', 'public-api', SPEC_THEME_FILENAME),
		destination: path.resolve(ROOT_DIR, 'dist', 'public-api'),
	};

	shell.cp('-r', swaggerTheme.source, swaggerTheme.destination);
}

function bundleOpenApiSpecs() {
	const publicApiDir = path.resolve(ROOT_DIR, 'src', 'public-api');

	shell
		.find(publicApiDir)
		.reduce((acc, cur) => {
			return cur.endsWith(SPEC_FILENAME) ? [...acc, path.relative('./src', cur)] : acc;
		}, [])
		.forEach((specPath) => {
			const distSpecPath = path.resolve(ROOT_DIR, 'dist', specPath);
			const command = `pnpm openapi bundle "src/${specPath}" --output "${distSpecPath}"`;

			shell.exec(command, { silent: true });
		});
}

function generateTimezoneData() {
	const timezones = ['Etc/UTC', 'Etc/GMT', ...rawTimeZones.map((tz) => tz.name)];
	const data = timezones.sort().reduce((acc, name) => {
		acc[name] = name.replaceAll('_', ' ');
		return acc;
	}, {});
	writeFileSync(path.resolve(ROOT_DIR, 'dist/timezones.json'), JSON.stringify({ data }));
}
