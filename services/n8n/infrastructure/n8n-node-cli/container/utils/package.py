"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/utils/package.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/utils 的工具。导入/依赖:外部:node:fs/promises、prettier；内部:无；本地:./filesystem、./json。导出:N8nPackageJson。关键函数/方法:updatePackageJson、getPackageJson、isN8nNodePackage、getPackageJsonNodes、setNodesPackageJson、addCredentialPackageJson。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/utils/package.ts -> services/n8n/infrastructure/n8n-node-cli/container/utils/package.py

import fs from 'node:fs/promises';
import path from 'node:path';
import prettier from 'prettier';

import { writeFileSafe } from './filesystem';
import { jsonParse } from './json';

export type N8nPackageJson = {
	name: string;
	version: string;
	n8n?: {
		nodes?: string[];
		credentials?: string[];
		strict?: boolean;
	};
};

export async function updatePackageJson(
	dirPath: string,
	updater: (packageJson: N8nPackageJson) => N8nPackageJson,
) {
	const packageJsonPath = path.resolve(dirPath, 'package.json');
	const packageJson = jsonParse<N8nPackageJson>(await fs.readFile(packageJsonPath, 'utf-8'));

	if (!packageJson) return;

	const updatedPackageJson = updater(packageJson);

	await writeFileSafe(
		packageJsonPath,
		await prettier.format(JSON.stringify(updatedPackageJson), { parser: 'json' }),
	);
}

export async function getPackageJson(dirPath: string) {
	const packageJsonPath = path.resolve(dirPath, 'package.json');
	const packageJson = jsonParse<N8nPackageJson>(await fs.readFile(packageJsonPath, 'utf-8'));

	return packageJson;
}

export async function isN8nNodePackage(dirPath = process.cwd()) {
	const packageJson = await getPackageJson(dirPath).catch(() => null);

	return Array.isArray(packageJson?.n8n?.nodes);
}

export async function getPackageJsonNodes(dirPath: string) {
	const packageJson = await getPackageJson(dirPath);
	return packageJson?.n8n?.nodes ?? [];
}

export async function setNodesPackageJson(dirPath: string, nodes: string[]) {
	await updatePackageJson(dirPath, (packageJson) => {
		packageJson['n8n'] ??= {};
		packageJson['n8n'].nodes = nodes;
		return packageJson;
	});
}

export async function addCredentialPackageJson(dirPath: string, credential: string) {
	await updatePackageJson(dirPath, (packageJson) => {
		packageJson['n8n'] ??= {};
		packageJson['n8n'].credentials ??= [];
		packageJson['n8n'].credentials.push(credential);
		return packageJson;
	});
}
