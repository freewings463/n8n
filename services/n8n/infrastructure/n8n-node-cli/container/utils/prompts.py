"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/utils/prompts.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/utils 的工具。导入/依赖:外部:@clack/prompts、node:fs/promises、picocolors；内部:无；本地:./json、./package。导出:onCancel。关键函数/方法:onCancel、cancel、ensureN8nPackage、getCliVersion、getCommandHeader、printCommandHeader。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/utils/prompts.ts -> services/n8n/infrastructure/n8n-node-cli/container/utils/prompts.py

import { cancel, isCancel, log } from '@clack/prompts';
import fs from 'node:fs/promises';
import path from 'node:path';
import picocolors from 'picocolors';

import { jsonParse } from './json';
import { isN8nNodePackage } from './package';

export async function withCancelHandler<T>(prompt: Promise<symbol | T>): Promise<T> {
	const result = await prompt;
	if (isCancel(result)) return onCancel();
	return result;
}

export const onCancel = (message = 'Cancelled', code = 0) => {
	cancel(message);
	process.exit(code);
};

export async function ensureN8nPackage(commandName: string) {
	const isN8nNode = await isN8nNodePackage();
	if (!isN8nNode) {
		log.error(`Make sure you are in the root directory of your node package and your package.json contains the "n8n" field

For example:
{
	"name": "n8n-nodes-my-app",
	"version": "0.1.0",
	"n8n": {
		"nodes": ["dist/nodes/MyApp.node.js"]
	}
}
`);
		onCancel(`${commandName} can only be run in an n8n node package`, 1);
		process.exit(1);
	}
}

async function getCliVersion(): Promise<string> {
	try {
		const packageJsonPath = path.join(__dirname, '..', '..', 'package.json');
		const content = await fs.readFile(packageJsonPath, 'utf-8');
		const packageJson = jsonParse<{ version: string }>(content);
		return packageJson?.version ?? 'unknown';
	} catch {
		return 'unknown';
	}
}

export async function getCommandHeader(commandName: string): Promise<string> {
	const version = await getCliVersion();
	return `${picocolors.inverse(` ${commandName} `)} ${picocolors.dim(`v${version}`)}`;
}

export async function printCommandHeader(commandName: string): Promise<void> {
	const header = await getCommandHeader(commandName);
	process.stdout.write(`${header}\n\n`);
}
