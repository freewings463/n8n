"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/utils/command-suggestions.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/node-cli/src/utils 的工具。导入/依赖:外部:picocolors；内部:无；本地:./package-manager。导出:formatCommand。关键函数/方法:getExecCommand、packageManager、formatCommand、suggestCloudSupportCommand、suggestLintCommand。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI package default -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/utils/command-suggestions.ts -> services/n8n/presentation/n8n-node-cli/cli/utils/command_suggestions.py

import picocolors from 'picocolors';

import { detectPackageManager } from './package-manager';

type ExecCommandType = 'cli' | 'script';

export async function getExecCommand(type: ExecCommandType = 'cli'): Promise<string> {
	const packageManager = (await detectPackageManager()) ?? 'npm';

	if (type === 'script') {
		return packageManager === 'npm' ? 'npm run' : packageManager;
	}

	return packageManager === 'npm' ? 'npx' : packageManager;
}

export function formatCommand(command: string): string {
	return picocolors.cyan(command);
}

export async function suggestCloudSupportCommand(action: 'enable' | 'disable'): Promise<string> {
	const execCommand = await getExecCommand('cli');
	return formatCommand(`${execCommand} n8n-node cloud-support ${action}`);
}

export async function suggestLintCommand(): Promise<string> {
	const execCommand = await getExecCommand('script');
	return formatCommand(`${execCommand} lint`);
}
